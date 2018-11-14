from collections import abc
from keyword import iskeyword


class FrozenJson:
    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, raw_data):
        self.__data = {}
        for key, value in raw_data.items():
            if iskeyword(key):
                key += "_"
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJson(self.__data[name])


grad = FrozenJson({"names": [{"hehe": "haha"}], "class": 1982, "2be": "not to be"})
print(grad.class_)
print(grad.names[0].hehe)
print(grad.__dict__)
