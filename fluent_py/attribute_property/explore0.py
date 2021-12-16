import json
from collections import abc


class FrozenJson:
    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        try:
            return getattr(self.__data, name)
        except AttributeError:
            return FrozenJson.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


if __name__ == "__main__":
    raw_feed = json.load(open("osconfeed.json"))
    feed = FrozenJson(raw_feed)
    print(len(feed.Schedule.speakers))
    print(feed.Schedule.keys())
    print(feed.Schedule.events[40].name)
    # 未处理key error
    # print(feed.not_exist)
    # 未处理保留字
    # print(feed.class)
    grad = FrozenJson({"name": "hehe", "class": 1982})
    print(getattr(grad, "class"))
