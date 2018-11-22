"""
在coroaverage1.average中，一旦我们send一个非数字引发异常之后，因为生成器未处理该异常将会被停止
"""
import inspect


class DemoException(Exception):
    pass


def demo_exc_handling():
    print("-> corotuine started")
    while True:
        try:
            x = yield
        except DemoException:
            print("***DemoException handled. Cortinuing...")
        else:
            print("-> corotuine received ", x)
    raise RuntimeError("this line should never be run")


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
exc_cor2.throw(ZeroDivisionError)
# 运行不到
print(inspect.getgeneratorstate(exc_cor2))
exc_cor2.send(22)
exc_cor2.close()