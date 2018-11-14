from collections import abc
from keyword import iskeyword


class FrozenJson:
    def __init__(self, raw_data):
        self.__data = {}
        for key, value in raw_data.items():
            # if iskeyword(key):
            #     key = key + "_"
            if key.isidentifier():
                key = "_" + key
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJson.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


grad = FrozenJson({"name": "hehe", "class": 1982, "2be": "not to be"})
print(grad._class)
print(grad.__dict__)
# SyntaxError: invalid syntax
# print(grad.2be)
# 尝试了不同方法，无法简便的识别出2be的无效性

