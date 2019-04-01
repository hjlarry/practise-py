# 不应该在Sentence类中去实现__next__方法，这是一种反模式的行为
# 迭代器设计模式可用来访问一个聚合对象的内容而不暴露其内部，支持对聚合对象的多种遍历，支持多态迭代
class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = text.split()
        self.words = {0: "haha", 1: "hehe", "he": 3}

    def __iter__(self):
        return SentenceIterator(self.words)


class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            word = self.words[self.index]
        except KeyError:
            raise StopIteration()
        self.index += 1
        return word


s = Sentence("hello world haha")

for word in s:
    print(word)
