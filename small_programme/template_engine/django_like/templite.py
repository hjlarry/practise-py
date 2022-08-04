"""
- 教程：http://aosabook.org/en/500L/pages/a-template-engine.html
- 中文教程：https://www.jianshu.com/p/b5d4aa45e771
- 作者源码：https://github.com/aosabook/500lines/blob/master/template-engine/template-engine.markdown?1533540328619
"""
import re


class TempliteSyntaxError(ValueError):
    """Raised when a template has a syntax error."""

    pass


# 源码构造器
class CodeBuilder:
    def __init__(self, indent=0):
        self.code = []
        self.indent_level = indent

    def __str__(self):
        return "".join(str(c) for c in self.code)

    def add_line(self, line):
        self.code.extend([" " * self.indent_level, line, "\n"])

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

    # 执行代码，并返回global字典
    def get_globals(self):
        assert self.indent_level == 0
        python_source = str(self)
        global_namespace = {}
        exec(python_source, global_namespace)
        return global_namespace


class Templite:
    """A simple template renderer, for a nano-subset of Django syntax.
    Supported constructs are extended variable access::
        {{var.modifer.modifier|filter|filter}}
    loops::
        {% for var in list %}...{% endfor %}
    and ifs::
        {% if var %}...{% endif %}
    Comments are within curly-hash markers::
        {# This will be ignored #}
    Construct a Templite with the template text, then use `render` against a
    dictionary context to create a finished string::
        templite = Templite('''
            <h1>Hello {{name|upper}}!</h1>
            {% for topic in topics %}
                <p>You are interested in {{topic}}.</p>
            {% endfor %}
            ''',
            {'upper': str.upper},
        )
        text = templite.render({
            'name': "Ned",
            'topics': ['Python', 'Geometry', 'Juggling'],
        })
    """

    def __init__(self, text, *contexts):
        """Construct a Templite with the given `text`.
        `contexts` are dictionaries of values to use for future renderings.
        These are good for filters and global values.
        """
        self.context = {}
        for context in contexts:
            self.context.update(context)
        self.all_vars = set()
        self.loop_vars = set()

        # 以源码的形式构造一个函数，然后编译并保存它，再执行它来渲染模板
        code = CodeBuilder()
        code.add_line("def render_function(context, do_dots):")
        code.indent()
        vars_code = code.add_section()
        code.add_line("result = []")
        code.add_line("append_result = result.append")
        code.add_line("extend_result = result.extend")
        code.add_line("to_str = str")

        bufferd = []

        def flush_output():
            # 把buffered的内容放到代码生成器
            if len(bufferd) == 1:
                code.add_line("append_result(%s)" % bufferd[0])
            elif len(bufferd) > 1:
                code.add_line("extend_result([%s])" % ", ".join(bufferd))
            del bufferd[:]

        ops_stack = []
        tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)
        for token in tokens:
            if token.startswith("{#"):
                # 模板中的注释内容不做处理
                continue
            elif token.startswith("{{"):
                # 直接执行的表达式
                expr = self._expr_code(token[2:-2].strip())
                bufferd.append("to_str(%s)" % expr)
            elif token.startswith("{%"):
                # 动作标签，需要进一步拆分和解析
                flush_output()
                words = token[2:-2].strip().split()
                if words[0] == "if":
                    if len(words) != 2:
                        self._synx_error("Don't understand if", token)
                    ops_stack.append("if")
                    code.add_line("if %s:" % self._expr_code(words[1]))
                    code.indent()
                elif words[0] == "for":
                    if len(words) != 4 or words[2] != "in":
                        self._synx_error("Don't understand for", token)
                    ops_stack.append("for")
                    self._variable(words[1], self.loop_vars)
                    code.add_line(
                        "for c_%s in %s:" % (words[1], self._expr_code(words[3]))
                    )
                    code.indent()
                elif words[0].startswith("end"):
                    if len(words) != 1:
                        self._synx_error("Don't understand end", token)
                    end_what = words[0][3:]
                    if not ops_stack:
                        self._synx_error("Too many ends", token)
                    start_what = ops_stack.pop()
                    if end_what != start_what:
                        self._synx_error("Mismatched end tag", end_what)
                    code.dedent()
                else:
                    self._synx_error("Don't understand tag", words[0])
            else:
                # 文字内容，如果不为空则直接输出
                if token:
                    bufferd.append(repr(token))

        if ops_stack:
            self._synx_error("Unmatched action tag", ops_stack[-1])
        flush_output()

        for varname in self.all_vars - self.loop_vars:
            vars_code.add_line("c_%s = context[%r]" % (varname, varname))

        code.add_line("return ''.join(result)")
        code.dedent()

        self._render_function = code.get_globals()["render_function"]

    def _expr_code(self, expr):
        # 给`expr`生成一个python表达式
        if "|" in expr:
            pipes = expr.split("|")
            code = self._expr_code(pipes[0])
            for func in pipes[1:]:
                self._variable(func, self.all_vars)
                code = "c_%s(%s)" % (func, code)
        elif "." in expr:
            dots = expr.split(".")
            code = self._expr_code(dots[0])
            args = ", ".join(repr(d) for d in dots[1:])
            code = "do_dots(%s, %s)" % (code, args)
        else:
            self._variable(expr, self.all_vars)
            code = "c_%s" % expr
        return code

    def _synx_error(self, msg, thing):
        """Raise a syntax error using `msg`, and showing `thing`."""
        raise TempliteSyntaxError("%s: %r" % (msg, thing))

    def _variable(self, name, vars_set):
        # 校验若name合法，则添加到vars_set中去
        if not re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", name):
            self._synx_error("Not a valid name", name)
        vars_set.add(name)

    def render(self, context=None):
        # 使用context字典来渲染模板
        render_context = dict(self.context)
        if context:
            render_context.update(context)
        return self._render_function(render_context, self._do_dots)

    def _do_dots(self, value, *dots):
        # 执行getattr操作
        for dot in dots:
            try:
                value = getattr(value, dot)
            except AttributeError:
                value = value[dot]
            if callable(value):
                value = value()
        return value


if __name__ == "__main__":
    templite = Templite(
        """
                <h1>Hello {{name|upper}}!</h1>
                {% for topic in topics %}
                    <p>You are interested in {{topic}}.</p>
                {% endfor %}
                """,
        {"upper": str.upper},
    )
    text = templite.render(
        {
            "name": "Ned",
            "topics": ["Python", "Geometry", "Juggling"],
        }
    )
    print(text)
