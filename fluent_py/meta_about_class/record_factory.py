# 这个函数创建的类不能去使用pickle序列化，而namedtuple对此是做了处理的


def record_factory(cls_name, field_names):
    try:
        field_names = field_names.replace(",", " ").split()
    except AttributeError:
        pass
    field_names = tuple(field_names)

    def __init__(self, *args, **kwargs):
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self):
        values = ", ".join("{}={!r}".format(*i) for i in zip(self.__slots__, self))
        return f"{self.__class__.__name__}({values})"

    class_attr = dict(
        __slots__=field_names, __init__=__init__, __iter__=__iter__, __repr__=__repr__
    )
    return type(cls_name, (object,), class_attr)


Dog = record_factory("Dog1", "name weight")
rex = Dog("Rex", 30)
print(rex)
print(Dog.__mro__)
