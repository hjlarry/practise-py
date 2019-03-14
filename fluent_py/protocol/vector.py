from array import array
import math
import reprlib
import numbers
import functools
import operator
import itertools


class Vector:
    type_code = "d"
    shortcut_names = 'xyzt'

    def __init__(self, components):
        self._components = array(self.type_code, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        class_name = type(self).__name__
        # reprlib.repr是长度过长时使用 ...
        components = reprlib.repr(self._components)
        # components是array的字符串形式，repr用list表示更友好
        components = components[components.find("["): -1]
        return "{}({})".format(class_name, components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.type_code)]) + bytes(self._components)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

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
        raise AttributeError(f'{cls.__name__!r} object has no attribute {name}')

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = 'readonly attr {attr_name!r}'
            elif name.islower():
                error = "can`t set attr 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True

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
        return outer_fmt.format(', '.join(components))


print(repr(Vector([3.1, 4.2])))
print(repr(Vector((3, 4, 5))))
print(repr(Vector(range(10))))

v1 = Vector(range(7))
print(v1[3:5])
print(v1.y)
print(format(v1, 'h'))
print(format(v1))