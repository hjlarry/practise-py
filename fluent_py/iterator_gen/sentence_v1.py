class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = text.split()
        # self.words = {0:'haha', 1:'hehe', 'he':3}

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)


s = Sentence("hello world haha")

for word in s:
    print(word)

"""
for循环相当于以下while代码，python从可迭代对象中获取迭代器。内置的iter函数作用:
1. 检查对象是否实现了__iter__方法，若实现则调用其返回的迭代器
2. 若未实现，但实现了__getitem__方法，则创建一个迭代器并尝试从index为0开始顺序获取元素
3. 若尝试失败，则抛出TypeError异常
"""
it = iter(s)
while True:
    try:
        print(next(it))
    except StopIteration:
        del it
        break


print()
from collections import abc


class Foo:
    def __iter__(self):
        pass


class Bar:
    def __next__(self):
        pass

    def __iter__(self):
        pass


"""
Iterator和Iterable去检查是否可迭代实际是因其实现的subclasshook方法检查类有否实现__iter__, 大致如下:
@classmethod
def __subclasshook__(cls, C):
    if(any("__next__" in B.__dict__ for B in C.__mro__) and 
        any("__iter__" in B.__dict__ for B in C.__mro__)):
        return True
    return NotImplemented
"""
print(issubclass(Foo, abc.Iterable))
print(issubclass(Bar, abc.Iterator))
print(issubclass(Sentence, abc.Iterable))
