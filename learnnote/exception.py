import dis

# 一、 执行机制
# def test():
#     try:
#         raise Exception
#     except:
#         print("except")


# dis.dis(test)
"""
➜  practise git:(master) ✗ /usr/local/bin/python3 /Users/hejl/local/practise/learnnote/exception.py
解释器使用块栈(block stack)结构处理异常逻辑，它和执行栈一起被栈帧管理。
  5           0 SETUP_EXCEPT             8 (to 10)      # 向块栈添加except跳转位置

  6           2 LOAD_GLOBAL              0 (Exception)  # 创建并引发异常
              4 RAISE_VARARGS            1              # 解释器从块栈弹出设置，按参数跳转
              6 POP_BLOCK
              8 JUMP_FORWARD            20 (to 30)

  7     >>   10 POP_TOP                                 # 跳转到此处
             12 POP_TOP                                 # 清楚exc参数
             14 POP_TOP

  8          16 LOAD_GLOBAL              1 (print)      # 执行except代码
             18 LOAD_CONST               1 ('except')
             20 CALL_FUNCTION            1
             22 POP_TOP
             24 POP_EXCEPT                              # 移除块栈内的设置
             26 JUMP_FORWARD             2 (to 30)      # 处理后函数正常返回
             28 END_FINALLY
        >>   30 LOAD_CONST               0 (None)
             32 RETURN_VALUE
"""
# 二、 异常对象的处理
# import traceback
# import sys


# def b():
#     # 发生异常时把异常对象保存在当前线程中
#     raise Exception("sdsd")


# def test():
#     try:
#         b()
#     except:
#         # 捕获时把异常对象从线程状态中清除
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         print(exc_value)
#         # traceack对象存储了栈桢、源码等信息
#         traceback.print_tb(exc_traceback)


# test()


# 三、 断言
# dis.dis(compile("assert True", "", "exec", optimize=0))
# dis.dis(compile("assert True", "", "exec", optimize=1))
"""
➜  practise git:(master) ✗ /usr/local/bin/python3 /Users/hejl/local/practise/learnnote/exception.py
  1           0 LOAD_CONST               0 (True)
              2 POP_JUMP_IF_TRUE         8
              4 LOAD_GLOBAL              0 (AssertionError)
              6 RAISE_VARARGS            1
        >>    8 LOAD_CONST               1 (None)
             10 RETURN_VALUE
  1           0 LOAD_CONST               0 (None)
              2 RETURN_VALUE
开启优化后，断言语句会被编译器忽略掉。

assert expresstion1, expresstion2
就相当于
if __debug__:
    if not expression1:
        raise AssertionError(expression2)
"""

# 四、上下文
"""
上下文管理协议是对异常处理结构的一种包装，它更利于重用。  
with expression [as var]:
    suite
对应的执行流程:
o = expression()  # 创建上下文对象
x = o.__enter__()  # 执行__enter__，将返回值导出到本地变量x，如果此时发生异常，则后续不会被执行
try:
    suite # 用户代码
except:
    typ, val, tb = sys.exc_info() # 拦截异常，传递给__exit__
finally:
    if not o.__exit__(typ, val, tb):  # 确保__exit__总会被执行，如果__exit__返回False，则重新抛出异常
        raise val
"""

# 已有代码逻辑，可以改造为上下文的包装
def test(db):
    print("open ", db)
    try:
        print("exec ", db)
    finally:
        print("close ", db)


import contextlib


@contextlib.contextmanager
def db_context(db):
    try:
        print("open ", db)
        yield db
    finally:
        print("close ", db)


def test1(db):
    with db_context(db):
        print("exec ", db)


test("sqlite")
test1("sqlite")
