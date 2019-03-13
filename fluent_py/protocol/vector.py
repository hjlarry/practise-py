from array import array
import math
import reprlib


class Vector:
    type_code = "d"

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

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        type_code = chr(octets[0])
        memv = memoryview(octets[1:]).cast(type_code)
        return cls(memv)

    # def angle(self):
    #     # 角度
    #     return math.atan2(self.y, self.x)
    #
    # def __format__(self, format_spec=""):
    #     # 如果以p结尾，那么在极坐标中显示向量
    #     if format_spec.endswith("p"):
    #         format_spec = format_spec[:-1]
    #         coords = (abs(self), self.angle())
    #         outer_fmt = "<{}, {}>"
    #     else:
    #         coords = self
    #         outer_fmt = "({}, {})"
    #     components = (format(c, format_spec) for c in coords)
    #     return outer_fmt.format(*components)
    #
    # def __hash__(self):
    #     return hash(self.x) ^ hash(self.y)


print(repr(Vector([3.1, 4.2])))
print(repr(Vector((3, 4, 5))))
print(repr(Vector(range(10))))

