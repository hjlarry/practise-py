import re


class Template:
    def __init__(self, text: str) -> None:
        self._text = text

    def render(self, ctx: dict) -> str:
        return self._text


class Token:
    def parse(self, content: str):
        raise NotImplementedError()

    def __eq__(self, other: object) -> bool:
        return type(self) == type(other) and repr(self) == repr(other)


class Text(Token):
    def __init__(self, content: str = None) -> None:
        self._content = content

    def parse(self, content: str):
        self._content = content

    def __repr__(self) -> str:
        return f"Text({self._content})"


class Expr(Token):
    def __init__(self, content: str = None) -> None:
        self._varname = content

    def parse(self, content: str):
        self._varname = content

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
