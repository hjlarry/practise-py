import re
from typing import Callable

OUTPUT_VAR = "_output_"
INDENT = 1
UNINDENT = -1
INDENT_SPACE = 2
INDEX_VAR = "index"


class Template:
    def __init__(self, text: str, filters: dict = None):
        self._text = text
        self._code = None
        self._global_vars = {}
        if filters:
            self._global_vars.update(filters)

    def _generate_code(self):
        if not self._code:
            tokens = tokenize(self._text)
            builder = CodeBuilder()
            for token in tokens:
                token.generate_code(builder)
            builder.check_code()
            source_code = builder.source()
            self._code = compile(source_code, "", "exec")

    def render(self, ctx: dict) -> str:
        self._generate_code()
        exec_ctx = ctx.copy()
        output = []
        exec_ctx[OUTPUT_VAR] = output
        exec_ctx["LoopVar"] = LoopVar
        exec(self._code, self._global_vars, exec_ctx)
        return "".join(output)


class TemplateEngine:
    def __init__(self):
        self._filters = {}
        self.register_filter("upper", lambda x: x.upper())
        self.register_filter("strip", lambda x: x.strip())

    def register_filter(self, name: str, filter_: Callable):
        self._filters[name] = filter_

    def create(self, text: str) -> Template:
        return Template(text, filters=self._filters)


class LoopVar:
    def __init__(self, index: int) -> None:
        self.index = index
        self.index0 = index
        self.index1 = index + 1


class CodeBuilder:
    def __init__(self) -> None:
        self.codes = []
        self._block_stack = []

    def add_code(self, line: str):
        self.codes.append(line)

    def add_expr(self, expr: str):
        code = f"{OUTPUT_VAR}.append(str({expr}))"
        self.codes.append(code)

    def add_text(self, text: str):
        code = f"{OUTPUT_VAR}.append({repr(text)})"
        self.codes.append(code)

    def indent(self):
        self.codes.append(INDENT)

    def unindent(self):
        self.codes.append(UNINDENT)

    def code_lines(self):
        indent = 0
        for code in self.codes:
            if isinstance(code, str):
                prefix = " " * indent * INDENT_SPACE
                line = prefix + code
                yield line
            elif code in (INDENT, UNINDENT):
                indent += code

    def source(self) -> str:
        return "\n".join(self.code_lines())

    def push_control(self, ctrl):
        self._block_stack.append(ctrl)

    def check_code(self):
        if self._block_stack:
            last_control = self._block_stack.pop(-1)
            raise SyntaxError(f"{last_control.name} has no end tag!")

    def end_block(self, begin_token_type):
        block_name = begin_token_type.name
        if not self._block_stack:
            raise SyntaxError(f"End of block {block_name} does not match start tag")
        top_block = self._block_stack.pop(-1)
        return top_block


class Token:
    def parse(self, content: str):
        raise NotImplementedError()

    def generate_code(self, builder: CodeBuilder):
        raise NotImplementedError()

    def __eq__(self, other: object) -> bool:
        return type(self) == type(other) and repr(self) == repr(other)


class Text(Token):
    def __init__(self, content: str = None):
        self._content = content

    def parse(self, content: str):
        self._content = content

    def generate_code(self, builder: CodeBuilder):
        builder.add_text(self._content)

    def __repr__(self) -> str:
        return f"Text({self._content})"


class Expr(Token):
    def __init__(self, content: str = None):
        self._varname = content
        self._filters = []

    def parse(self, content: str):
        self._varname, self._filters = parse_expr(content)

    def generate_code(self, builder: CodeBuilder):
        result = self._varname
        for filter_name in self._filters[::-1]:
            result = f"{filter_name}({result})"
        builder.add_expr(result)

    def __repr__(self) -> str:
        if self._filters:
            return f"Expr({self._varname} | {' | '.join(self._filters)})"
        return f"Expr({self._varname})"


class Comment(Token):
    def __init__(self, content: str = None):
        self._content = content

    def parse(self, content: str):
        self._content = content

    def generate_code(self, builder: CodeBuilder):
        pass

    def __repr__(self) -> str:
        return f"Comment({self._content})"


class For(Token):
    name = "for"

    def __init__(self, var_name: str = None, target: str = None) -> None:
        self._var_name = var_name
        self._target = target

    def parse(self, content: str):
        m = re.match(r"for\s+(\w+)\s+in\s+(\w+)", content)
        if not m:
            raise SyntaxError(f"invalid for block:{content}")
        self._var_name, self._target = m.group(1), m.group(2)

    def generate_code(self, builder: CodeBuilder):
        builder.add_code(
            f"for {INDEX_VAR}, {self._var_name} in enumerate({self._target}):"
        )
        builder.indent()
        builder.push_control(self)
        builder.add_code(f"loop = LoopVar({INDEX_VAR})")

    def __repr__(self) -> str:
        return f"For({self._var_name} in {self._target})"


class EndFor(Token):
    def parse(self, content: str):
        pass

    def generate_code(self, builder: CodeBuilder):
        builder.unindent()
        builder.end_block(For)

    def __repr__(self) -> str:
        return "EndFor"


class If(Token):
    name = "if"

    def __init__(self, expr: str = None) -> None:
        self._expr = expr

    def parse(self, content: str):
        m = re.match(r"if\s+(\w+)", content)
        if not m:
            raise SyntaxError(f"invalid if block:{content}")
        self._expr = m.group(1)

    def generate_code(self, builder: CodeBuilder):
        builder.add_code(f"if {self._expr}:")
        builder.indent()
        builder.push_control(self)

    def __repr__(self) -> str:
        return f"If({self._expr})"


class Elif(Token):
    def __init__(self, expr: str = None) -> None:
        self._expr = expr

    def parse(self, content: str):
        m = re.match(r"elif\s+(\w+)", content)
        if not m:
            raise SyntaxError(f"invalid else if block:{content}")
        self._expr = m.group(1)

    def generate_code(self, builder: CodeBuilder):
        builder.unindent()
        builder.add_code(f"elif {self._expr}:")
        builder.indent()

    def __repr__(self) -> str:
        return f"Elif({self._expr})"


class Else(Token):
    def parse(self, content: str):
        pass

    def generate_code(self, builder: CodeBuilder):
        builder.unindent()
        builder.add_code("else:")
        builder.indent()

    def __repr__(self) -> str:
        return "Else"


class EndIf(Token):
    def parse(self, content: str):
        pass

    def generate_code(self, builder: CodeBuilder):
        builder.unindent()
        builder.end_block(If)

    def __repr__(self) -> str:
        return "EndIf"


def tokenize(text: str) -> list[Token]:
    segments = re.split(r"({{.*?}}|{#.*?#}|{%.*?%})", text)
    return [create_token(s) for s in segments if s]


def create_token(text: str) -> Token:
    if text.startswith("{{") and text.endswith("}}"):
        token, content = Expr(), text[2:-2].strip()
    elif text.startswith("{#") and text.endswith("#}"):
        token, content = Comment(), text[2:-2].strip()
    elif text.startswith("{%") and text.endswith("%}"):
        content = text[2:-2].strip()
        token = create_control_token(content)
    else:
        token, content = Text(), text
    token.parse(content)
    return token


def create_control_token(text: str) -> Token():
    m = re.match(r"^(\w+)", text)
    if not m:
        raise SyntaxError(f"Unknown token {text}")
    keyword = m.group(1)
    token_types = {
        "for": For,
        "endfor": EndFor,
        "if": If,
        "elif": Elif,
        "else": Else,
        "endif": EndIf,
    }
    if keyword not in token_types:
        raise SyntaxError(f"Unknown control token {text}")
    return token_types[keyword]()


def extract_last_filter(text: str) -> tuple[str, str]:
    m = re.search(r"(\|\s*[A-Za-z0-9_]+\s*)$", text)
    if m:
        suffix = m.group(1)
        filter = suffix[1:].strip()
        var_name = text[: -len(suffix)].strip()
        return var_name, filter
    return text, None


def parse_expr(text: str) -> tuple[str, list[str]]:
    var_name, filters = text, []
    while True:
        var_name, filter_ = extract_last_filter(var_name)
        if filter_:
            filters.insert(0, filter_)
        else:
            break
    return var_name, filters
