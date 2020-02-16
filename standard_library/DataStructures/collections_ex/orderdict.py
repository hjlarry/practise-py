import collections

# OrderedDict 内部维护着一个根据键插入顺序排序的双向链表，所以它的大小是一个普通字典的两倍

print("一、字典只验证内容是否相等，orderdict还验证插入顺序")
d1 = {}
d1["a"] = "A"
d1["b"] = "B"
d1["c"] = "C"

d2 = {}
d2["c"] = "C"
d2["a"] = "A"
d2["b"] = "B"
print(d1 == d2)

d1 = collections.OrderedDict()
d1["a"] = "A"
d1["b"] = "B"
d1["c"] = "C"

d2 = collections.OrderedDict()
d2["c"] = "C"
d2["a"] = "A"
d2["b"] = "B"
print(d1 == d2)
print()


print("二、move_to_end方法")
print("Before:")
for k, v in d1.items():
    print(k, v)
print("move_to_end(last=False):")
d1.move_to_end("b", last=False)
for k, v in d1.items():
    print(k, v)
print("move_to_end():")
d1.move_to_end("b")
for k, v in d1.items():
    print(k, v)
