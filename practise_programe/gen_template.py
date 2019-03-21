"""
- 教程：http://aosabook.org/en/500L/pages/a-template-engine.html
- 中文教程：https://www.jianshu.com/p/b5d4aa45e771
- 作者源码：https://github.com/aosabook/500lines/blob/master/template-engine/template-engine.markdown?1533540328619
"""
import re

from exceptions import TempliteSyntaxError


class CodeBuilder(object):
    def __init__(self, indent=0):
        self.code = []
        self.indent_level = indent

    def __str__(self):
        return ''.join(str(c) for c in self.code)

    def add_line(self, line):
        self.code.extend([' ' * self.indent_level, line, '\n'])

    INDENT_STEP = 4

    # 缩进方法
    def indent(self):
        self.indent_level += self.INDENT_STEP

    def dedent(self):
        self.indent_level -= self.INDENT_STEP

    # 参考位置
    def add_section(self):
        section = CodeBuilder(self.indent_level)
        self.code.append(section)
        return section

    def get_globals(self):
        assert self.indent_level == 0
        python_source = str(self)
        global_namespace = {}
        exec(python_source, global_namespace)
        return global_namespace


class Templite(object):
    def __init__(self, text, *contexts):
        self.context = {}
        for context in contexts:
            self.context.update(context)
        self.all_vars = set()
        self.loop_vars = set()

        code = CodeBuilder()
        code.add_line('def render_function(context, do_dots):')
        code.indent()
        vars_code = code.add_section()
        code.add_line('result = []')
        code.add_line('append_result = result.append')
        code.add_line('extend_result = result.extend')
        code.add_line('to_str = str')

        bufferd = []
        def flush_output():
            if len(bufferd) == 1:
                code.add_line('append_result(%s)' % bufferd[0])
            elif len(bufferd) > 1:
                code.add_line('extend_result([%s])' % ', '.join(bufferd))
            del bufferd[:]

        ops_stack = []
        tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)
        for token in tokens:
            if token.startswith('{#'):
                # 模板中的注释内容不做处理
                continue
            elif token.startswith('{{'):
                expr = self._expr_code(token[2:-2].strip())
                bufferd.append('to_str(%s)' % expr)
            elif token.startswith('{%'):
                flush_output()
                words = token[2:-2].strip().split()
                if words[0] == 'if':
                    if len(words) != 2:
                        self._synx_error('Don`t understand for if: %s' % token)
                    ops_stack.append('if')
                    code.add_line('if %s:' % self._expr_code(words[1]))
                elif words[0] == 'for':
                    if len(words) != 4 or words[2] != 'in':
                        self._synx_error('Don`t understand for for: %s' % token)
                    ops_stack.append('for')
                    self._variable(words[1], self.loop_vars)
                    code.add_line('for %s in %s:' % (words[1], self._expr_code(words[3])))
                    code.indent()
                elif words[0].startswith('end'):
                    if len(words) != 1:
                        self._synx_error('Don`t understand for end: %s' % token)
                    end_what = words[0][3:]
                    if not ops_stack:
                        self._synx_error('too many end : %s' % token)
                    start_what = ops_stack.pop()
                    if end_what != start_what:
                        self._synx_error('mismatch end tag : %s' % end_what)
                    code.dedent()
                else:
                    self._synx_error('unknown start tag: %s' % token)
            else:
                if token:
                    bufferd.append(repr(token))

        if ops_stack:
            self._synx_error('Unmatch action tag: %s' % ops_stack[-1])
        flush_output()

        for varname in self.all_vars - self.loop_vars:
            vars_code.add_line('c_%s = context[%r]' % (varname, varname))

        code.add_line("return ''.join(result)")
        code.dedent()

        self._render_function = code.get_globals()['render_function']

    def _expr_code(self, expr):
        if '|' in expr:
            pipes = expr.split('|')
            code = self._expr_code(pipes[0])
            for func in pipes[1:]:
                self._variable(func, self.all_vars)
                code = 'c_%s(%s)' % (func, code)
        elif '.' in expr:
            dots = expr.split('.')
            code = self._expr_code(dots[0])
            args = ', '.join(repr(d) for d in dots[1:])
            code = 'do_dots(%s, %s)' % (code, args)
        else:
            self._variable(expr, self.all_vars)
            code = 'c_%s' % expr
        return code

    def _synx_error(self, msg):
        raise TempliteSyntaxError(msg)

    def _variable(self, name, vars_set):
        if not re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", name):
            self._synx_error('not a valid name : %s' % name)
        vars_set.add(name)

    def render(self, context=None):
        render_context = dict(self.context)
        if context:
            render_context.update(context)
        return self._render_function(render_context, self._do_dots)

    def _do_dots(self, value, **dots):
        for dot in dots:
            try:
                value = getattr(value, dot)
            except AttributeError:
                value = value[dot]
            if callable(value):
                value = value()
        return value

