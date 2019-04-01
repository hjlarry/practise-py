import abc

# 或 class PluginBase(metaclass=abc.ABCMeta)
class PluginBase(abc.ABC):
    @abc.abstractmethod
    def load(self, input):
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, output, data):
        raise NotImplementedError


class LocalBaseClass:
    pass


@PluginBase.register
class RegisteredImplementation(LocalBaseClass):
    def load(self, input):
        return input.read()

    def save(self, output, data):
        return output.write(data)


print("Subclass:", issubclass(RegisteredImplementation, PluginBase))
print("Instance:", isinstance(RegisteredImplementation(), PluginBase))


class SubclassImplementation(PluginBase):
    def load(self, input):
        return input.read()

    def save(self, output, data):
        return output.write(data)


print("Subclass:", issubclass(SubclassImplementation, PluginBase))
print("Instance:", isinstance(SubclassImplementation(), PluginBase))


for sc in PluginBase.__subclasses__():
    print(sc.__name__)

# 类和静态方法同样可被标记为抽象的
class Base(abc.ABC):
    @property
    @abc.abstractmethod
    def value(self):
        return "never get here"

    @value.setter
    @abc.abstractmethod
    def value(self, new_value):
        return


class PartialImplementation(Base):
    @property
    def value(self):
        return "read only"


class Implementation(Base):
    _value = "default value"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


try:
    b = Base()
except Exception as err:
    print(err)

p = PartialImplementation()
print("Partial Implement:", p.value)

try:
    p.value = "haha"
except Exception as err:
    print(err)

i = Implementation()
print(i.value)
i.value = 123
print(i.value)
