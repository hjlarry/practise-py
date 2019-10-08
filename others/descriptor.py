# 使用描述符实现 @property，@staticmethod，@classmethod


class MyProperty:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, obj, obj_type=None):
        print("in __get__")
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError
        return self.fget(obj)

    def __set__(self, obj, value):
        print("in __set__")
        if self.fset is None:
            raise AttributeError
        return self.fset(obj, value)

    def __delete__(self, obj):
        print("in __delete__")
        if self.fdel is None:
            raise AttributeError
        return self.fdel(obj)

    def setter(self, fset):
        print("in setter")
        return type(self)(self.fget, fset, self.fdel, self.__doc__)


class MyStaticmethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, obj_type=None):
        return self.func


class MyClassmethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, owner=None):
        def new_func(*args):
            return self.func(owner, *args)

        return new_func


class Student:
    def __init__(self, name):
        self.name = name
        self._score = 0

    @MyProperty
    def score(self):
        return self._score

    # score的get和set其实对应了MyProperty类的两个实例，只是为什么获取值时进入第一个实例，而赋值会进入第二个实例。背后是什么逻辑？
    @score.setter
    def score(self, value):
        if value < 0:
            print("error score")
        else:
            self._score = value

    @MyStaticmethod
    def hello():
        return 9527

    @MyClassmethod
    def hi(cls, what):
        return what


a = Student("xiaoming")
print(a.score)
a.score = -10
print(a.score)
a.score = 100
print(a.score)

print(a.hello())
print(Student.hi(888))
