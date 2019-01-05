import collections

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
