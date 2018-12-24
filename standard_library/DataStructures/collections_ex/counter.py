import collections

print(collections.Counter(["a", "b", "c", "a"]))
print(collections.Counter(a=2, b=3))
print(collections.Counter({"a": 2, "b": 4}))
print()

c = collections.Counter()
print("init:", c)
c.update("abbad")
print("seq:", c)
c.update({"a": 1})
print("dict:", c)
print()

c = collections.Counter("abc")
print(c["d"])  # 不会抛 KeyError 异常

c["z"] = 0
print(c)
print(list(c.elements()))
print()

c = collections.Counter()

with open("/usr/share/dict/words", "rt") as f:
    for line in f:
        c.update(line.rstrip().lower())

print("Most common:")
for letter, count in c.most_common(3):
    print(f"{letter}:{count}")


c1 = collections.Counter("abbad")
c2 = collections.Counter("alpha")

print("c1:", c1)
print("c2:", c2)
print("combined:", c1 + c2)
print("subtraction:", c1 - c2)
print("Intersection:", c1 & c2)
print("union:", c1 | c2)
