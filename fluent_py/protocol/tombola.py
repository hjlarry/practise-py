"""
尽量不要自己定义抽象基类，除非要构建允许用户扩展的框架，然而大多数情况并非如此
"""

import abc
import random


class Tombola(abc.ABC):
    @abc.abstractmethod
    def load(self, iterable):
        """从可迭代对象中添加元素"""

    # 如果有其他装饰器，abstractmethod应该在最里层
    @abc.abstractmethod
    def pick(self):
        """随机删除元素并返回它，实例为空则应抛出`LookupError`"""

    def loaded(self):
        """如果至少有一个元素，返回true。
        抽象基类的实现效率不高"""
        return bool(self.inspect())

    def inspect(self):
        """返回由当前元素构成的有序元组。
        抽象基类的实现比较笨拙，全取出再放回"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))


class BingoCage(Tombola):
    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError("pick from empty BingoCage")

    def __call__(self):
        self.pick()


class LotteryBlower(Tombola):
    def __init__(self, iterable):
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError("pick from empty LotteryBlower")
        return self._balls.pop(position)

    def loaded(self):
        """覆盖基类方法提升效率"""
        return bool(self._balls)

    def inspect(self):
        """覆盖基类方法提升效率"""
        return tuple(sorted(self._balls))


# 注册虚拟子类，并不会继承基类的任何方法，只是为了isinstance, 需要自己全部实现
@Tombola.register
class TomboList(list):
    def pick(self):
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError("pop from empty TomboList")

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))


print(issubclass(TomboList, Tombola))
t = TomboList(range(100))
print(isinstance(t, Tombola))
print(t.pick())
# mro中没有抽象基类
print(TomboList.__mro__)
# __subclasses__只能得到直接子类
print(Tombola.__subclasses__())
# _abc_registry会得到虚拟子类的弱引用，即WeakSet对象
print(list(Tombola._abc_registry))
