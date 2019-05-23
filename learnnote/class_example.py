from collections import defaultdict
import weakref

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


# 示例三、 状态机


class Connection:
    """普通方案，好多个判断语句，效率低下"""

    def __init__(self):
        self.state = "CLOSED"

    def read(self):
        if self.state != "OPEN":
            raise RuntimeError("Not open")
        print("reading")

    def write(self, data):
        if self.state != "OPEN":
            raise RuntimeError("Not open")
        print("writing")

    def open(self):
        if self.state == "OPEN":
            raise RuntimeError("Already open")
        self.state = "OPEN"

    def close(self):
        if self.state == "CLOSED":
            raise RuntimeError("Already closed")
        self.state = "CLOSED"


class Connection1:
    """新方案——对每个状态定义一个类"""

    def __init__(self):
        self.new_state(ClosedConnectionState)

    def new_state(self, newstate):
        self._state = newstate

    def read(self):
        return self._state.read(self)

    def write(self, data):
        return self._state.write(self, data)

    def open(self):
        return self._state.open(self)

    def close(self):
        return self._state.close(self)


# Connection state base class
class ConnectionState:
    @staticmethod
    def read(conn):
        raise NotImplementedError()

    @staticmethod
    def write(conn, data):
        raise NotImplementedError()

    @staticmethod
    def open(conn):
        raise NotImplementedError()

    @staticmethod
    def close(conn):
        raise NotImplementedError()


# Implementation of different states
class ClosedConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        raise RuntimeError("Not open")

    @staticmethod
    def write(conn, data):
        raise RuntimeError("Not open")

    @staticmethod
    def open(conn):
        conn.new_state(OpenConnectionState)

    @staticmethod
    def close(conn):
        raise RuntimeError("Already closed")


class OpenConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        print("reading")

    @staticmethod
    def write(conn, data):
        print("writing")

    @staticmethod
    def open(conn):
        raise RuntimeError("Already open")

    @staticmethod
    def close(conn):
        conn.new_state(ClosedConnectionState)


c = Connection1()
print(c._state)
try:
    c.read()
except Exception as e:
    print(e.args)
c.open()
print(c._state)
c.read()
c.write("hello")
c.close()
print(c._state)


# 示例四、 创建缓存实例
# 创建一个对象时，如果之前使用同样参数创建过这个对象， 则返回它的缓存引用
class CachedSpamManager:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get_spam(self, name):
        if name not in self._cache:
            s = Spam(name)
            self._cache[name] = s
        else:
            s = self._cache[name]
        return s

    def clear(self):
        self._cache.clear()

# 不应直接去初始化，而是用类方法get_spam
class Spam:
    manager = CachedSpamManager()

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_spam(cls, name):
        return Spam.manager.get_spam(name)


a = Spam.get_spam("foo")
b = Spam.get_spam("foo")
c = Spam.get_spam("bar")
print(a is b)
print(a is c)
