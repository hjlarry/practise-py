import inspect


def simple_cor():
    c = 20
    print("started, c=", c)
    yield 1
    a = yield c
    print("received, a=", a)
    b = yield a + c
    print("received, b=", b)


my_cor = simple_cor()
# generator 有4个状态: GEN_CREATED/GEN_RUNNING/GEN_SUSPENDED/GEN_CLOSED
print(inspect.getgeneratorstate(my_cor))
# 预激生成器 next(gen) 或 gen.send(None)都可以
next(my_cor)
print(inspect.getgeneratorstate(my_cor))
my_cor.send(99)
print(inspect.getgeneratorstate(my_cor))
print(my_cor.send(999))  # send的同时也会receive值
print(inspect.getgeneratorstate(my_cor))
try:
    print(next(my_cor))
except StopIteration:
    pass
print(inspect.getgeneratorstate(my_cor))

my_cor1 = simple_cor()
next(my_cor1)
next(my_cor1)
next(my_cor1)
next(my_cor1)
next(my_cor1)
