"""
关于运算符重载
"""

from array import array
import math
import reprlib
import numbers
import functools
import operator
import itertools


class Vector:
    type_code = "d"
    shortcut_names = "xyzt"

    def __init__(self, components):
        self._components = array(self.type_code, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        class_name = type(self).__name__
        # reprlib.repr是长度过长时使用 ...
        components = reprlib.repr(self._components)
        # components是array的字符串形式，repr用list表示更友好
        components = components[components.find("[") : -1]
        return "{}({})".format(class_name, components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.type_code)]) + bytes(self._components)

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        type_code = chr(octets[0])
        memv = memoryview(octets[1:]).cast(type_code)
        return cls(memv)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        # 若传入切片，则也能返回一个Vector对象，而不是array
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            raise TypeError(f"{cls.__name__} indices must be integers")

    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        raise AttributeError(f"{cls.__name__!r} object has no attribute {name}")

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = "readonly attr {attr_name!r}"
            elif name.islower():
                error = "can`t set attr 'a' to 'z' in {cls_name!r}"
            else:
                error = ""
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        # reduce函数0是初始值
        return functools.reduce(operator.xor, hashes, 0)

    def angle(self, n):
        # wiki上的n维球体公式计算角坐标
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n - 1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, format_spec=""):
        # h结尾，超球面坐标
        if format_spec.endswith("h"):
            format_spec = format_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())
            outer_fmt = "<{}>"
        else:
            coords = self
            outer_fmt = "({})"
        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(", ".join(components))

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    """Start From Here"""

    def __neg__(self):
        # 一元取负算术运算符，例x==-2，则-x==2
        return Vector(-x for x in self)

    def __pos__(self):
        # 一元取负算术运算符，通常x == +x
        return Vector(self)

    def __add__(self, other):
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)
            return Vector(a + b for a, b in pairs)
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        # add的反向版本，例如a+b，若a对象未实现__add__，则会尝试调用b的__radd__
        return self + other

    def __mul__(self, scalar):
        # 标量积，scalar需要是数字
        if isinstance(scalar, numbers.Real):
            return Vector(n * scalar for n in self)
        else:
            return NotImplemented

    def __rmul__(self, scalar):
        return self * scalar

    def __matmul__(self, other):
        # 点积，即矩阵乘法，运算符是@，py3.5以上支持
        try:
            return sum(a * b for a, b in zip(self, other))
        except TypeError:
            return NotImplemented

    def __rmatmul__(self, other):
        return self @ other

    def __eq__(self, other):
        if isinstance(other, Vector):
            return len(self) == len(other) and all(a == b for a, b in zip(self, other))
        else:
            return NotImplemented


v1 = Vector([1, 3])
v2 = Vector([2, 4, 5.5])
print(v1 + v2)
print(v1 + (2, 20))
print(v1 * 14)
from v2d_not_slot import Vector2d

v3 = Vector2d(1, 3)
# 尽管Vector的__eq__做了验证右侧实例是否是Vector，但python得到NotImplemented仍会尝试调用Vector2d的__eq__，所以是true
print(v1 == v3)
