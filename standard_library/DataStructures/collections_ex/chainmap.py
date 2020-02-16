import collections

print("一、 基础操作")
a = {"a": "A", "c": "C"}
b = {"b": "B", "c": "D"}

m = collections.ChainMap(a, b)
print(f"a={m['a']}")
print(f"b={m['b']}")
print(f"c={m['c']}")  # 只会读取第一个c
print(f"keys={list(m.keys())}")
print(f"values={list(m.values())}")
print("Items:", end=" ")
for k, v in m.items():
    print(f"{k} = {v}", end=" ")
print()
print()

print("maps:", m.maps)
print(f"c={m['c']}")
m.maps = list(reversed(m.maps))
print("reverse maps:", m.maps)
print(f"get another c: c={m['c']}")
print()

print("二、 改变ChainMap中元素的值")
m = collections.ChainMap(a, b)
print(f"before: {m['c']}")
a["c"] = "E"
print(f"改变字典a中某key的值: {m['c']}")
print()

a1 = {"a": "A", "c": "C"}
b1 = {"b": "B", "c": "D"}
m1 = collections.ChainMap(a1, b1)
print(f"before: {m1}")
m1["c"] = "E"
print(f"直接改变ChainMap中某key的值: {m1}")
print("字典a1也跟着改变:", a1)
print()

m2 = m1.new_child()
print(f"m1 before: {m1}")
print(f"m2=m1.new_child(), m2: {m2}")
m2["a"] = "E"
print("改变m2中某key的值:")
print(f"m1 after: {m1}")
print(f"m2 after: {m2}")
print()

a = {"a": "A", "c": "C"}
b = {"b": "B", "c": "D"}
c = {"c": "E"}
print("m2=m1.new_child(c):")
m1 = collections.ChainMap(a, b)
m2 = m1.new_child(c)
print(f"m1 c = {m1['c']}")
print(f"m2 c = {m2['c']}")
