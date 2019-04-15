from collections import defaultdict

# 示例一、避免__init__中大量的初始化赋值
class Structure:
    _fields = []

    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError("Expected {} arguments".format(len(self._fields)))

        # Set all of the positional arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)

        # Set the remaining keyword arguments
        for name in self._fields[len(args) :]:
            setattr(self, name, kwargs.pop(name))

        # Check for any remaining unknown arguments
        if kwargs:
            raise TypeError("Invalid argument(s): {}".format(",".join(kwargs)))


class Stock(Structure):
    _fields = ["name", "shares", "price"]


s1 = Stock("ACME", 50, 91.1)
s2 = Stock("ACME", 50, price=91.1)
s3 = Stock("ACME", shares=50, price=91.1)
# s3 = Stock('ACME', shares=50, price=91.1, aa=1)


# 示例二、 混入类的使用
# 混入类不能直接被实例化使用。
# 混入类没有自己的状态信息，也就是说它们并没有定义 __init__() 方法，并且没有实例属性


class LoggedMappingMixin:
    """
    Add logging to get/set/delete operations for debugging.
    """

    __slots__ = ()  # 混入类都没有实例变量，因为直接实例化混入类没有任何意义

    def __getitem__(self, key):
        print("Getting " + str(key))
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        print("Setting {} = {!r}".format(key, value))
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        print("Deleting " + str(key))
        return super().__delitem__(key)


class SetOnceMappingMixin:
    """
    Only allow a key to be set once.
    """

    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + " already set")
        return super().__setitem__(key, value)


class StringKeysMappingMixin:
    """
    Restrict keys to strings only
    """

    __slots__ = ()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError("keys must be strings")
        return super().__setitem__(key, value)


class LoggedDict(LoggedMappingMixin, dict):
    pass


d = LoggedDict()
d["x"] = 23
print(d["x"])
del d["x"]


class SetOnceDefaultDict(SetOnceMappingMixin, defaultdict):
    pass


d = SetOnceDefaultDict(list)
d["x"].append(2)
d["x"].append(3)
# d['x'] = 23  # KeyError: 'x already set'


# 使用类装饰器替代多重继承的方案
def LoggedMapping(cls):
    """第二种方式：使用类装饰器"""
    cls_getitem = cls.__getitem__
    cls_setitem = cls.__setitem__
    cls_delitem = cls.__delitem__

    def __getitem__(self, key):
        print("Getting " + str(key))
        return cls_getitem(self, key)

    def __setitem__(self, key, value):
        print("Setting {} = {!r}".format(key, value))
        return cls_setitem(self, key, value)

    def __delitem__(self, key):
        print("Deleting " + str(key))
        return cls_delitem(self, key)

    cls.__getitem__ = __getitem__
    cls.__setitem__ = __setitem__
    cls.__delitem__ = __delitem__
    return cls


@LoggedMapping
class LoggedDict2(dict):
    pass
