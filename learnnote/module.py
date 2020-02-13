# 一、 模块
# import types
# import sys


# print(isinstance(sys, types.ModuleType))
# print(vars(sys) is sys.__dict__)  # vars返回目标的__dict__属性
# print(dir(sys))  # dir返回目标，或当前名字空间可访问的名字列表
# print(sys.modules)
# print(sys.path)  # 搜索路径

# 二、 成员导入和模块导入指令上有些许差异
# def a():
#     import sys

#     print(sys.version)


# def b():
#     from sys import version

#     print(version)


# import dis

# dis.dis(a)
# dis.dis(b)
"""
➜  practise git:(master) ✗ /usr/local/bin/python3 /Users/hejl/local/practise/learnnote/module.py
 14           0 LOAD_CONST               1 (0)
              2 LOAD_CONST               0 (None)
              4 IMPORT_NAME              0 (sys)
              6 STORE_FAST               0 (sys)

 16           8 LOAD_GLOBAL              1 (print)
             10 LOAD_FAST                0 (sys)        # 一条FAST指令
             12 LOAD_ATTR                2 (version)
             14 CALL_FUNCTION            1
             16 POP_TOP
             18 LOAD_CONST               0 (None)
             20 RETURN_VALUE
 20           0 LOAD_CONST               1 (0)
              2 LOAD_CONST               2 (('version',))
              4 IMPORT_NAME              0 (sys)        # 两条指令
              6 IMPORT_FROM              1 (version)
              8 STORE_FAST               0 (version)
             10 POP_TOP

 22          12 LOAD_GLOBAL              2 (print)
             14 LOAD_FAST                0 (version)
             16 CALL_FUNCTION            1
             18 POP_TOP
             20 LOAD_CONST               0 (None)
             22 RETURN_VALUE
"""

# 三、 动态导入
# 使用exec
import sys


def test1(name):
    exec(f"import {name}")
    m = sys.modules[name]
    print(m)


test1("dis")
# 使用importlib
import importlib


def test2(name):
    m = importlib.import_module(name)
    print(m)


test2("os")

