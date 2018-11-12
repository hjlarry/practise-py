import re

RE_WORD = re.compile(r"\w+")


class Sentence:
    def __init__(self, text):
        self.text = text

    def __iter__(self):
        # re.finditer 是 re.findall的惰性版本
        for match in RE_WORD.finditer(self.text):
            yield match.group()


s = Sentence("hello world haha")

for word in s:
    print(word)


class Sentence2:
    def __init__(self, text):
        self.text = text

    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))


s = Sentence2("hello world haha")

for word in s:
    print(word)
