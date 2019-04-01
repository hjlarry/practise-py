import gc
import pprint


class Graph:
    def __init__(self, name):
        self.name = name
        self.next = None

    def set_next(self, next):
        print(f"link nodes {self}.next={next}")
        self.next = next

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __del__(self):
        print(f"{self}.__del__()")


one = Graph("one")
two = Graph("two")
three = Graph("three")
one.set_next(two)
two.set_next(three)
three.set_next(one)

print("Collecting...")
n = gc.collect()
print("unreachable objs: ", n)
print("Remaining Garbage:")
pprint.pprint(gc.garbage)

# 定义我们要从本模块的本地变量，全局变量和垃圾回收器自己的记录中忽略一些引用
REFERERS_TO_IGNORE = [locals(), globals(), gc.garbage]


def find_referring_graphs(obj):
    print("looking for reference to ", obj)
    referers = (r for r in gc.get_referrers(obj) if r not in REFERERS_TO_IGNORE)
    for ref in referers:
        if isinstance(ref, Graph):
            yield ref
        elif isinstance(ref, dict):
            for parent in find_referring_graphs(ref):
                yield parent


print()
print("clearing referrers:")
for obj in [one, two, three]:
    for ref in find_referring_graphs(obj):
        print("found referrer:", ref)
        ref.set_next(None)
        del ref
    del obj

print()
print("clearing gc.garbage:")
del gc.garbage[:]

print("Collecting...")
n = gc.collect()
print("unreachable objs: ", n)
print("Remaining Garbage:")
pprint.pprint(gc.garbage)
