from collections import abc
from osconfeed import load


class FrozenJson:
    def __init__(self, raw_data):
        self.__data = dict(raw_data)

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


raw_feed = load()
feed = FrozenJson(raw_feed)
print(len(feed.Schedule.speakers))
print(feed.Schedule.keys())
print(feed.Schedule.events[40].name)
# 未处理key error
# print(feed.not_exist)
# 未处理保留字
# print(feed.class)
