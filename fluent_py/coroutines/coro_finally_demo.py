# 和coro_exc_demo.py对比
import inspect


class DemoException(Exception):
    pass


def demo_exc_handling():
    print("-> corotuine started")
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print("***DemoException handled. Cortinuing...")
            else:
                print("-> corotuine received ", x)
    finally:
        print("-> corotunie ending")


exc_cor = demo_exc_handling()
next(exc_cor)
exc_cor.send(11)
exc_cor.send(22)
exc_cor.close()
print(inspect.getgeneratorstate(exc_cor))
print()

exc_cor1 = demo_exc_handling()
next(exc_cor1)
exc_cor1.send(11)
exc_cor1.throw(DemoException)
print(inspect.getgeneratorstate(exc_cor1))
exc_cor1.send(22)
exc_cor1.close()
print()

exc_cor2 = demo_exc_handling()
next(exc_cor2)
exc_cor2.send(11)
# exc_cor2.throw(ZeroDivisionError)
# # 仍然运行不到
# print(inspect.getgeneratorstate(exc_cor2))
# exc_cor2.send(22)
# exc_cor2.close()

def another_gen_func():
    try:
        yield 1
    except BaseException:
        pass
    yield 2
    yield 3

gen = another_gen_func()
print(next(gen))
# GeneratorExit 不是 Exception的子类，它们都继承自BaseException
gen.throw(GeneratorExit)
print("hello")