import collections

print("示例一、使用函数创建默认值")


def default_factory():
    return "default value"


d = collections.defaultdict(default_factory, foo="bar")
print(d)
print(d["foo"])
print(d["hello"])


print("示例二")

d = collections.defaultdict(set)
d['a'].add(1)
d['a'].add(2)
d['b'].add(4)
print(d)