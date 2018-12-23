import collections

a = {"a": "A", "c": "C"}
b = {"b": "B", "c": "D"}

m = collections.ChainMap(a, b)
print(f"a={m['a']}")
print(f"b={m['b']}")
print(f"c={m['c']}")
print(f"keys={list(m.keys())}")
print(f"values={list(m.values())}")
print("Items:")
for k, v in m.items():
    print(f"{k} = {v}")
print(f"d in m? {'d' in m}")
print()

print(m.maps)
print(f"c={m['c']}")
m.maps = list(reversed(m.maps))
print(m.maps)
print(f"c={m['c']}")
print()

m = collections.ChainMap(a, b)
print(f"before: {m['c']}")
a["c"] = "E"
print(f"after: {m['c']}")
print()

a1 = {"a": "A", "c": "C"}
b1 = {"b": "B", "c": "D"}
m1 = collections.ChainMap(a1, b1)
print(f"before: {m1}")
m1["c"] = "E"
print(f"after: {m1}")
print("a:", a1)
print()

m2 = m1.new_child()
print(f"m1 before: {m1}")
print(f"m2 before: {m2}")
m2["a"] = "E"
print(f"m1 after: {m1}")
print(f"m2 after: {m2}")
print()

a = {"a": "A", "c": "C"}
b = {"b": "B", "c": "D"}
c = {"c": "E"}
m1 = collections.ChainMap(a, b)
m2 = m1.new_child(c)
print(f"m1 c = {m1['c']}")
print(f"m2 c = {m2['c']}")

