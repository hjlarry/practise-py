# 一、 装饰器
# 1. 类装饰器作用于某实例方法时，导致方法绑定丢失，引发异常
# class log1:
#     def __init__(self, fn):
#         self.fn = fn

#     def __call__(self, *args, **kwargs):
#         print("log ", *args, **kwargs)
#         return self.fn(*args, **kwargs)


# def log2(fn):
#     def wrap(*args, **kwargs):
#         print("log ", *args, **kwargs)
#         return fn(*args, **kwargs)

#     return wrap


# class X:
#     @log1
#     def test1(self):
#         return 5

#     @log2
#     def test2(self):
#         return 5


# x = X()
# x.test2()
# x.test1()

# 2. 作用于类的装饰器即可以用类写，也可以用函数写
# 用类写
# def log1(cls):
#     class wrapper:
#         def __init__(self, *args, **kwargs):
#             self.__dict__["inst"] = cls(*args, **kwargs)

#         def __getattr__(self, name):
#             value = getattr(self.inst, name)
#             print("get value ", value)
#             return value

#         def __setattr__(self, name, value):
#             print("set value", value)
#             return setattr(self.inst, name, value)

#     return wrapper


# # 用函数写
# def log2(cls):
#     def wrapper(*args, **kwargs):
#         o = cls(*args, **kwargs)
#         print("log ", o)
#         return o

#     return wrapper


# @log1
# class X:
#     pass


# @log2
# class Y:
#     pass


# X().a = 1

# Y().a = 1

# 3. 可用来跟踪调用
# def call_count(fn):
#     def counter(*args, **kwargs):
#         counter.__count__ += 1
#         return fn(*args, **kwargs)

#     counter.__count__ = 0
#     return counter


# @call_count
# def b():
#     pass


# b()
# b()
# b()
# print(b.__count__)

# 4. 可实现属性的管理，例如为目标添加额外的属性
# def pet(cls):
#     cls.dosth = lambda self: None
#     return cls


# @pet  # 添加宠物功能
# class Parrot:
#     pass

# 5. 可实现实例的管理，例如单例模式
# def singleton(cls):
#     inst = None

#     def wrap(*args, **kwargs):
#         nonlocal inst
#         if not inst:
#             inst = cls(*args, **kwargs)
#         return inst

#     return wrap


# @singleton
# class X:
#     pass


# print(X() is X())

# 6. 实现部件注册，例如web框架中的路由
# class App:
#     def __init__(self):
#         self.routers = {}

#     def route(self, url):
#         def register(fn):
#             self.routers[url] = fn
#             return fn

#         return register


# app = App()


# @app.route("/")
# def home():
#     pass


# @app.route("/help")
# def help():
#     pass


# print(app.routers)


# 二、 描述符
# 1. 一个完整的描述符实现
# class descriptor:
#     def __set_name__(self, owner, name):
#         print(f"name:{owner.__name__},,{name}")
#         self.name = f"__{name}__"

#     def __get__(self, instance, owner):
#         print(f"get:{instance}, {owner}")
#         return getattr(instance, self.name, None)

#     def __set__(self, instance, value):
#         print(f"set:{instance}, {value}")
#         return setattr(instance, self.name, value)

#     def __delete__(self, instance):
#         print(f"delete: {instance}")


# class X:
#     # 此时创建属性，自动调用__set_name__
#     data = descriptor()


# x = X()
# x.data  # __get__ 被调用
# x.data = 500  # __set__ 被调用
# del x.data  # __del__ 被调用
# # 以类型访问时，只有__get__会被调用
# X.data
# X.data = 100
# del X.data


# 2. 方法执行的步骤伪代码
# x.test(123) -->
#     m = x.test.__get__(x, type(x)) # 先将函数包装为绑定方法
#     m(123)  # 执行
#             --> X.test(m.__self__, 123) # 执行时，隐式传入self/cls参数给目标函数

# 3. 自己使用描述符实现 @property，@staticmethod，@classmethod
# class MyProperty:
#     def __init__(self, fget=None, fset=None, fdel=None, doc=None):
#         self.fget = fget
#         self.fset = fset
#         self.fdel = fdel
#         self.__doc__ = doc

#     def __get__(self, obj, obj_type=None):
#         print("in __get__")
#         if obj is None:
#             return self
#         if self.fget is None:
#             raise AttributeError
#         return self.fget(obj)

#     def __set__(self, obj, value):
#         print("in __set__")
#         if self.fset is None:
#             raise AttributeError
#         return self.fset(obj, value)

#     def __delete__(self, obj):
#         print("in __delete__")
#         if self.fdel is None:
#             raise AttributeError
#         return self.fdel(obj)

#     def setter(self, fset):
#         print("in setter")
#         return type(self)(self.fget, fset, self.fdel, self.__doc__)


# class MyStaticmethod:
#     def __init__(self, func):
#         self.func = func

#     def __get__(self, obj, obj_type=None):
#         return self.func


# class MyClassmethod:
#     def __init__(self, func):
#         self.func = func

#     def __get__(self, obj, owner=None):
#         def new_func(*args):
#             return self.func(owner, *args)

#         return new_func


# class Student:
#     def __init__(self, name):
#         self.name = name
#         self._score = 0

#     @MyProperty
#     def score(self):
#         return self._score

#     @score.setter
#     def score(self, value):
#         if value < 0:
#             print("error score")
#         else:
#             self._score = value

#     @MyStaticmethod
#     def hello():
#         return 9527

#     @MyClassmethod
#     def hi(cls, what):
#         return what


# a = Student("xiaoming")
# print(a.score)
# a.score = -10
# print(a.score)
# a.score = 100
# print(a.score)

# print(a.hello())
# print(Student.hi(888))


# 三、元类
# 1. 直接使用type可创建类
# User = type(
#     "User1",
#     (object,),
#     {
#         "__init__": lambda self, name: setattr(self, "name", name),
#         "test": lambda self: print(self.name),
#     },
# )
# print(User.__dict__)
# u = User("hello")
# u.test()
# u.a = 1
# print(u.__dict__)

# 2. 自定义元类，控制类型对象生成过程
# class DemoMeta(type):  # 继承自type
#     @classmethod
#     def __prepare__(cls, name, bases):
#         print(cls, name, bases)
#         print(f"__prepare__:{name}")
#         return {"__make__": "some make in DemoMeta"}  # 定制名字空间

#     def __new__(cls, name, bases, attrs):
#         print(f"__new__:{name}, {bases}, {attrs}")
#         return type.__new__(cls, name, bases, attrs)  # 创建并返回类型对象

#     def __init__(self, name, bases, attrs):
#         print(f"__init__:{self}, {name},")
#         return type.__init__(self, name, bases, attrs)  # 初始化后，返回类型对象

#     def __call__(cls, *args, **kwargs):
#         print(f"__call__:{cls}, {args}, {kwargs}")
#         return type.__call__(cls, *args, **kwargs)  # 调用类型对象创建实例过程，返回实例


# class X(metaclass=DemoMeta):
#     data = 100

#     def __init__(self, x, y):
#         self.x = y

#     def test(self):
#         pass


# o = X(5, 6)  # 调用元类的__call__

# 3. 元类可用来实现静态类， 阻止某类创建实例
# class StaticClassMeta(type):
#     def __call__(cls, *args, **kwargs):
#         raise RuntimeError("can`t create obj for static class")


# class X(metaclass=StaticClassMeta):
#     pass


# o = X()

# 4. 元类可用来实现密封类，阻止某类被继承
class SealedClassMeta(type):
    types = set()

    def __init__(cls, name, bases, attrs):
        if cls.types & set(bases):
            raise RuntimeError("can`t inherit from sealed class")
        cls.types.add(cls)


class A(metaclass=SealedClassMeta):
    pass


class B(A):
    pass
