import dis

# 一、反汇编类的创建过程
# def test():
#     class X:
#         data = 100

#         def get(self):
#             return self.data


# dis.dis(test)
"""
➜  practise git:(master) ✗ /usr/local/bin/python3 /Users/hejl/local/practise/learnnote/about_class.py
  5           0 LOAD_BUILD_CLASS
              2 LOAD_CONST               1 (<code object X at 0x10c314300, file "/Users/hejl/local/practise/learnnote/about_class.py", line 5>)
              4 LOAD_CONST               2 ('X')
              6 MAKE_FUNCTION            0
              8 LOAD_CONST               2 ('X')
             10 CALL_FUNCTION            2          # 调用的__build_class__函数
             12 STORE_FAST               0 (X)
             14 LOAD_CONST               0 (None)
             16 RETURN_VALUE
先创建‘X函数’，其内容是属性设置和方法创建，也就是<code object X at 0x10c314300>。
随后该函数被当作参数传入buildins.__build_class__函数调用，其实就是元类的执行。
接着是‘X函数’内部的执行过程。
Disassembly of <code object X at 0x10c314300, file "/Users/hejl/local/practise/learnnote/about_class.py", line 5>:
  5           0 LOAD_NAME                0 (__name__)
              2 STORE_NAME               1 (__module__)
              4 LOAD_CONST               0 ('test.<locals>.X')
              6 STORE_NAME               2 (__qualname__)

  6           8 LOAD_CONST               1 (100)
             10 STORE_NAME               3 (data)

  8          12 LOAD_CONST               2 (<code object get at 0x10c1e74b0, file "/Users/hejl/local/practise/learnnote/about_class.py", line 8>)
             14 LOAD_CONST               3 ('test.<locals>.X.get')
             16 MAKE_FUNCTION            0
             18 STORE_NAME               4 (get)
             20 LOAD_CONST               4 (None)
             22 RETURN_VALUE

Disassembly of <code object get at 0x10c1e74b0, file "/Users/hejl/local/practise/learnnote/about_class.py", line 8>:
  9           0 LOAD_FAST                0 (self)
              2 LOAD_ATTR    
"""

# # 二、类型都有自己的名字空间


# class A:
#     a = 10

#     def test_a(self):
#         return self.a


# class B(A):
#     b = 8

#     def __init__(self, bb):
#         self.bb = bb


# o = B(bb=10)
# # 类和实例都有自己的名字空间，继承并不继承名字空间
# print(A.__dict__)
# print(B.__dict__)
# print(o.__dict__)
# # 类的名字空间是只读的mappingproxy类型，实例的名字空间就是可修改的普通dict
# print(type(B.__dict__))
# print(type(o.__dict__))


# 三、继承
class A:
    pass


class B(A):
    pass


class C(B, A):
    pass


print(A.__class__)
print(A.__subclasses__())
# 按mro返回全部基类
print(C.__bases__)
# 返回单个基类
print(C.__base__)
print(C.__mro__)

print(vars(C))

print(isinstance(int, object))
print(isinstance(int, type))
print(isinstance(type, object))
print(isinstance(object, type))
print()
print(issubclass(object, type))
print(issubclass(type, object))
print(issubclass(int, object))
print(issubclass(int, type))


# 四、 对象属性查找顺序的伪码
# https://www.zhihu.com/question/25391709/answer/30634637
"""
def class_lookup(cls, name):
    "Look for attribute /name/ in class /cls/ and bases."
    v = cls.__dict__.get(name)
    if v is not None:
        # found in this class
        return v, cls
    # search in base classes
    for i in cls.__bases__:
        v, c = class_lookup(i, name)
        if v is not None:
            return v, c
    # not found
    return None


def object_getattr(obj, name):
    "Look for attribute /name/ in object /obj/."
    # First look in class and base classes.
    v, cls = class_lookup(obj.__class__, name)
    if (v is not None) and hasattr(v, "__get__") and hasattr(v, "__set__"):
        # Data descriptor.  Overrides instance member.
        return v.__get__(obj, cls)
    w = obj.__dict__.get(name)
    if w is not None:
        # Found in object
        return w
    if v is not None:
        if hasattr(v, "__get__"):
            # Function-like descriptor.
            # 如果v是一个方法，那么func本身实现了描述符协议，应该会走这里处理
            return v.__get__(obj, cls)
        else:
            # Normal data member in class
            return v
    raise AttributeError(obj.__class__, name)
"""
