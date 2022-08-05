class Template:
    def __init__(self, text: str) -> None:
        self._text = text

    def render(self, ctx: dict) -> str:
        return self._text
