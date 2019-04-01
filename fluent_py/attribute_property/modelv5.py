import abc


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
