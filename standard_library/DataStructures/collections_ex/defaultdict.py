import collections


def default_factory():
    return "default value"


d = collections.defaultdict(default_factory, foo="bar")
print(d)
print(d["foo"])
print(d["hello"])
