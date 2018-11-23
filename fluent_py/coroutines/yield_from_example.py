from itertools import chain

a = range(3)
b = "ABC"
c = dict((("a", 1), ("b", 2)))

for item in chain(a, b, c):
    print(item)
print()


def my_chain(*args):
    for iterable in args:
        for item in iterable:
            yield item


for item in my_chain(a, b, c):
    print(item)
print()


def my_yield(*args):
    for iterable in args:
        yield from iterable


for item in my_yield(a, b, c):
    print(item)
print()
