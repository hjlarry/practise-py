# # 一、 函数组成
# def test(x, y=10):
#     x += y
#     print(x, y)


# print(test)  # 函数对象
# print(test.__code__)  # 代码对象
# print(test.__code__.co_varnames)  # 参数及变量名列表
# print(test.__code__.co_consts)  # 指令常量
# print(test.__defaults__)  # 参数默认值
# test.__defaults__ = (1357,)  # 修改默认值
# test(1)  # 生效

# 二、 函数创建
# def make(n):
#     ret = []
#     for i in range(n):

#         def test():
#             print("hello")

#         # 相同的代码对象，不同的函数对象，说明def只是运行期创建函数实例
#         print(id(test), id(test.__code__))
#     return ret


# make(3)


# # 三、 闭包的实现
# def make():
#     x = 100
#     b = 1

#     def test():
#         print(x)

#     return test


# import dis

# dis.dis(make)

# """
# ➜  practise git:(master) ✗ /usr/local/bin/python3 /Users/hejl/local/practise/learnnote/function.py
#  33           0 LOAD_CONST               1 (100)
#               2 STORE_DEREF              0 (x)  # 环境变量存储从FAST区转移至DEREF区

#  34           4 LOAD_CONST               2 (1)
#               6 STORE_FAST               0 (b)  # 环境变量存储在FAST区

#  36           8 LOAD_CLOSURE             0 (x)  # 闭包环境变量
#              10 BUILD_TUPLE              1
#              12 LOAD_CONST               3 (<code object test at 0x1077ba4b0, file "/Users/hejl/local/practise/learnnote/function.py", line 36>)
#              14 LOAD_CONST               4 ('make.<locals>.test')
#              16 MAKE_FUNCTION            8      # 创建函数时包含闭包参数
#              18 STORE_FAST               1 (test)

#  39          20 LOAD_FAST                1 (test)
#              22 RETURN_VALUE

# Disassembly of <code object test at 0x1077ba4b0, file "/Users/hejl/local/practise/learnnote/function.py", line 36>:
#  37           0 LOAD_GLOBAL              0 (print)
#               2 LOAD_DEREF               0 (x)  # 从DEREF中载入x
#               4 CALL_FUNCTION            1
#               6 POP_TOP
#               8 LOAD_CONST               0 (None)
#              10 RETURN_VALUE
# """
# f = make()
# print(f.__closure__)  # 闭包所引用的环境变量保存在__closure__中
# print(f.__code__.co_freevars)  # 当前函数引用的外部自由变量元组
# print(make.__code__.co_cellvars)  # 被内部闭包函数引用的变量列表


# # 四、 延迟绑定
# def make(n):
#     f = []
#     for i in range(n):
#         f.append(lambda: print(i))
#     return f


# # 自由变量i的值在执行函数时才引用到
# a, b, c = make(3)
# a()
# b()
# c()


# 五、 栈桢
import sys
import inspect


def A():
    x = "hello"
    B()


def B():
    C()


def C():
    f = sys._getframe(2)  # 向上2级，获取栈帧
    print(f.f_code)  # A代码对象
    print(f.f_locals)  # 运行期获取A的名字空间
    print(f.f_lasti)  # A最后执行指令的偏移量（以确定继续执行的位置）
    print(sys._current_frames())  # 文档更推荐用inspect模块
    for ff in inspect.stack():
        print(ff.function, ff.lineno)


A()


# 六、 便函数伪代码
def partial(func, *part_args, **part_kwargs):  # 偏函数伪代码
    def wrap(*call_args, **call_kwargs):
        kwargs = part_kwargs.copy()  # 复制包装键值参数
        kwargs.update(call_kwargs)  # 使用调用键值参数更新包装键值参数
        return func(*part_args, *call_args, **kwargs)

    return wrap
