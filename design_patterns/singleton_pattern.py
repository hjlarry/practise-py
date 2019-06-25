print("一、推荐方法：Borg模式替代单例模式")

# 其实每新建一个对象其id是不同的，只是共享了状态和属性
class Borg:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.state = "Init"

    def __str__(self):
        return self.state


class YourBorg(Borg):
    pass


rm1 = Borg()
rm2 = Borg()

rm1.state = "Idle"
rm2.state = "Running"

print("rm1: {0}".format(rm1))
print("rm2: {0}".format(rm2))

rm2.state = "Zombie"

print("rm1: {0}".format(rm1))
print("rm2: {0}".format(rm2))

print("rm1 id: {0}".format(id(rm1)))
print("rm2 id: {0}".format(id(rm2)))

rm3 = YourBorg()

print("rm1: {0}".format(rm1))
print("rm2: {0}".format(rm2))
print("rm3: {0}".format(rm3))
print()


print("二、使用装饰器")


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


@singleton
class Foo(object):
    pass


foo1 = Foo()
foo2 = Foo()

print(foo1 is foo2)
print()


print("三、使用__new__")


class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class Foo(Singleton):
    pass


foo1 = Foo()
foo2 = Foo()
print(foo1 is foo2)
print()


print("四、使用元类")


class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Foo(metaclass=Singleton):
    pass


foo1 = Foo()
foo2 = Foo()
print(foo1 is foo2)
