import collections


class Text(collections.UserString):
    def __repr__(self):
        return f"Text({self.data!r})"

    def reverse(self):
        return self[::-1]


word = Text("forward")
print(word)
print(word.reverse())
print(Text.reverse(Text("backward")))
print(Text.reverse("repaid"))  # type:ignore
print(type(Text.reverse), type(word.reverse))
print(Text.reverse.__get__(word))  # type:ignore
print(Text.reverse.__get__(None, Text))  # type:ignore
print(word.reverse)
print(word.reverse.__self__)  # type:ignore
print(word.reverse.__func__ is Text.reverse)  # type:ignore
