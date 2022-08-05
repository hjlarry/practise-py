import re


OUTPUT_VAR = "_output_"


class Template:
    def __init__(self, text: str) -> None:
        self._text = text
        self._code = None

    def _generate_code(self):
        if not self._code:
            tokens = tokenize(self._text)
            code_lines = [x.generate_code() for x in tokens]
            source_code = "\n".join(code_lines)
            self._code = compile(source_code, "", "exec")

    def render(self, ctx: dict) -> str:
        self._generate_code()
        exec_ctx = ctx.copy()
        output = []
        exec_ctx[OUTPUT_VAR] = output
        exec(self._code, None, exec_ctx)
        return "".join(output)


class Token:
    def parse(self, content: str):
        raise NotImplementedError()

    def generate_code(self) -> str:
        raise NotImplementedError()

    def __eq__(self, other: object) -> bool:
        return type(self) == type(other) and repr(self) == repr(other)


class Text(Token):
    def __init__(self, content: str = None) -> None:
        self._content = content

    def parse(self, content: str):
        self._content = content

    def generate_code(self) -> str:
        return f"{OUTPUT_VAR}.append({repr(self._content)})"

    def __repr__(self) -> str:
        return f"Text({self._content})"


class Expr(Token):
    def __init__(self, content: str = None) -> None:
        self._varname = content

    def parse(self, content: str):
        self._varname = content

    def generate_code(self) -> str:
        return f"{OUTPUT_VAR}.append(str({self._varname}))"

    def __repr__(self) -> str:
        return f"Expr({self._varname})"


def tokenize(text: str) -> list[Token]:
    segments = re.split(r"({{.*?}})", text)
    return [create_token(s) for s in segments if s]


def create_token(text: str) -> Token:
    if text.startswith("{{") and text.endswith("}}"):
        token, content = Expr(), text[2:-2].strip()
    else:
        token, content = Text(), text
    token.parse(content)
    return token
