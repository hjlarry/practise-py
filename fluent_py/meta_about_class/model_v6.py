import abc
import collections


class AutoStorage:
    __counter = 0

    def __init__(self):
        self.storage_name = f"_{self.__class__.__name__}#{self.__class__.__counter}"
        self.__class__.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            # 解决类似 LineItem.weight这样的访问问题
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)


class Validated(abc.ABC, AutoStorage):
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validate(self, instance, value):
        """Return validated value or raise error"""


class Quantity(Validated):
    def validate(self, instance, value):
        if value <= 0:
            raise ValueError("value must > 0")
        return value


class NoneBlank(Validated):
    def validate(self, instance, value):
        value = value.strip()
        if len(value) == 0:
            raise ValueError("value must not blank")
        return value


def entity(cls):
    for key, attr in cls.__dict__.items():
        if isinstance(attr, Validated):
            type_name = type(attr).__name__
            attr.storage_name = f"_{type_name}#{key}"
    return cls


class EntityMeta(type):
    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        for key, attr in attr_dict.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = f"_{type_name}#{key}"


class Entity(metaclass=EntityMeta):
    pass


class EntityMetaWithPrepare(type):
    # 添加了__prepare__方法后，__init__中的attrdict会从__prepare__中得到，但实际上貌似用处不大
    @classmethod
    def __prepare__(cls, name, bases):
        return dict(a=222)
        # return collections.OrderedDict()

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        cls._field_names = []
        print(attr_dict.keys())
        for key, attr in attr_dict.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = f"_{type_name}#{key}"
                cls._field_names.append(key)


class EntityPrepare(metaclass=EntityMetaWithPrepare):
    @classmethod
    def field_names(cls):
        for name in cls._field_names:
            yield name
