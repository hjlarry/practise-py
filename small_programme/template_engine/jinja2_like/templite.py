import re
from typing import Callable

OUTPUT_VAR = "_output_"
INDENT = 1
UNINDENT = -1
INDENT_SPACE = 2


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
            source_code = builder.source()
            self._code = compile(source_code, "", "exec")

    def render(self, ctx: dict) -> str:
        self._generate_code()
        exec_ctx = ctx.copy()
        output = []
        exec_ctx[OUTPUT_VAR] = output
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


class CodeBuilder:
    def __init__(self) -> None:
        self.codes = []

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
    def __init__(self, var_name: str = None, target: str = None) -> None:
        self._var_name = var_name
        self._target = target

    def parse(self, content: str):
        m = re.match(r"for\s+(\w+)\s+in\s+(\w+)", content)
        if not m:
            raise SyntaxError(f"invalid block:{content}")
        self._var_name, self._target = m.group(1), m.group(2)

    def __repr__(self) -> str:
        return f"For({self._var_name} in {self._target})"


class EndFor(Token):
    def parse(self, content: str):
        pass

    def __repr__(self) -> str:
        return "EndFor"


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
