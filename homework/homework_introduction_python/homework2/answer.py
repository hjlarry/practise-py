import re

# Question 2
s0_255 = "(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})"
s_ip = re.match(s0_255 + "\." + s0_255 + "\." + s0_255 + "\." + s0_255, "0.168.1.1")

# Question 3.1
date = re.match(
    "(?P<year>\d{4})\-(?P<month>1[012]|0\d)\-(?P<day>[0-2]\d|3[01])", "2018-05-31"
).groupdict()
print("{}/{}/{}".format(date["month"], date["day"], date["year"]))

# Question 3.2
def convert(s):
    s = re.findall("([A-Z][a-z]*)", s)
    s = [word.lower() for word in s]
    return "_".join(s)


print(convert("HowToCOnvertWords"))

# Question 3.3
ID_NAMES = {"U1EAT8MG9": "xiaoming", "U0K1MF23Z": "laolin"}
s = "<@U1EAT8MG9>, <@U0K1MF23Z> 嗯 确实是这样的"


def search_uid():
    return "|".join(dict.fromkeys(ID_NAMES))


def match(ma):
    return ID_NAMES[ma.group()]


res = re.sub(search_uid(), match, s)
print(res)

# Question 4
def _fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


g = _fib()


def fib(n):
    return next(g)


print([fib(n) for n in range(16)])


# Question 5
import os
import click


@click.command()
@click.option("--level", default=1, help="Descend only level directories deep")
@click.option("--path", help="directory path name")
def main(level, path):
    """list contents of directories in a tree-like format."""
    list_file(level, path)


def list_file(level, path, pos=0):
    path = "." if path is None else path
    dirs = os.listdir(path)
    for dir in dirs:
        click.echo("   " * pos + "|--" + dir)
        if os.path.isdir(dir) and level > 0:
            list_file(level - 1, dir, pos + 1)


# Question 6
def injectArguments(fn):
    def wrapper(*args, **kwargs):
        args[0].__dict__.update(kwargs)
        return fn(*args, **kwargs)

    return wrapper


class Test:
    @injectArguments
    def __init__(self, x, y, z):
        pass


t = Test(x=4, y=5, z=6)
print(t.x, t.y, t.z)


# Question 7
import time


class Timed:
    def __enter__(self):
        self.t1 = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Cost:{time.time()-self.t1}")

    def __call__(self, fn):
        def wrapper():
            t1 = time.time()
            fn()
            print(f"Cost:{time.time()-t1}")

        return wrapper


# with Timed():
#     time.sleep(2)
#
# @Timed()
# def f():
#     time.sleep(2)
# f()


# Question 8
class Seq:
    def __init__(self, *args):
        self.data = args[0] if len(args) == 1 else args

    def map(self, args):
        number = list(map(args, self.data))
        return Seq(number)

    def filter(self, args):
        number = list(filter(args, self.data))
        return Seq(number)

    def reduce(self, args):
        from functools import reduce

        number = reduce(args, self.data)
        return Seq(number)

    def __repr__(self):
        return str(self.data)


# print(Seq(1, 2, 3, 4).map(lambda x: x * 2).filter(lambda x: x > 4).reduce(lambda x, y: x + y))


# Question 9
with open("something", "rb") as f:
    for chunk in f:
        pass
