import abc


class Validated(abc.ABC):
    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        value = self.validate(instance, value)
        instance.__dict__[self.storage_name] = value

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
