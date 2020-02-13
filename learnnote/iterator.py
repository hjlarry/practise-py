# # 一、迭代器
# class Data:
#     def __init__(self, n):
#         self.data = list(range(n))

#     def __iter__(self):
#         return DataIter(self.data)


# class DataIter:
#     def __init__(self, data):
#         self.data = data
#         self.index = 0

#     def __next__(self):
#         if not self.data or self.index >= len(self.data):
#             raise StopIteration

#         d = self.data[self.index]
#         self.index += 1
#         return d


# d = Data(2)
# for i in d:
#     print(i)

# x = d.__iter__()
# print(next(x))  # Iterator才能用next，d本身不是iterator
# print(next(x))
# # print(next(x))  # StopIteration

# # 使用内置的iter函数便于创建iterator
# class Data2:
#     def __init__(self, n):
#         self.data = list(range(n))

#     def __iter__(self):
#         return iter(self.data)


# d2 = Data2(2)
# y = d2.__iter__()
# print(next(y))
# print(next(y))


# # 二、 生成器
# def test(n):
#     print("gen start")
#     for i in range(n):
#         print("gen yield ", i)
#         yield i
#         print("gen.resume")


# print(test.__code__.co_flags)  # 编译器在编译的时候发现是生成器，则添加一个标记
# import inspect

# print(inspect.isgeneratorfunction(test))  # 也可通过inspect判断是否是生成器

# x = test(2)
# print(x.__next__)  # 实现迭代器协议方法
# print("first next:")
# x.__next__()
# print("second next:")
# x.__next__()
# print("third next:")
# x.__next__()


# 三、 生成器的双向通讯
# def test():
#     while True:
#         v = yield 200
#         print("resume ", v)


# x = test()
# print(x.send(None))  # 必须先发送None或用next()预激生成器，这里返回200
# x.send("dsdsd")
# x.close()  # 终止生成器


# 四、 使用生成器实现生产消费模式
# def consumer():
#     while True:
#         x = yield
#         print("consume:", x)


# def producer(c):
#     for i in range(3):
#         c.send(i)


# c = consumer()
# c.send(None)
# producer(c)
# c.close()


# 五、 使用生成器消除回调
# 回调模式
# import time
# import threading


# def target(request, callback):
#     request()  # 调用请求函数
#     time.sleep(2)  # 模拟阻塞情况
#     callback("sth")  #  调用回调函数


# def service(request, callback):
#     threading.Thread(target=target, args=(request, callback)).start()


# def request():
#     print("request start")


# def callback(x):
#     print(x)


# service(request, callback)

# # 消除回调的生成器模式, 消除碎片化
# def request1():
#     print("request start1")
#     x = yield
#     print(x)


# def target1(fn):
#     try:
#         g = fn()
#         g.send(None)
#         time.sleep(2)
#         g.send("sth1")
#     except StopIteration:
#         pass


# def service1(fn):
#     threading.Thread(target=target1, args=(fn,)).start()


# service1(request1)


# 六、 使用生成器实现协程
# def sched(*tasks):
#     tasks = list(map(lambda t: t(), tasks))  # 调用所有任务函数，一个生成器的列表
#     while tasks:
#         try:
#             t = tasks.pop(0)  # 列表头部弹出任务
#             t.send(None)  # 开始执行
#             tasks.append(t)  # 如果任务没有结束，则放回列表尾部
#         except StopIteration:  # 任务结束，丢弃
#             pass


# from functools import partial


# def task(id, n, m):
#     for i in range(n, m):
#         print(f"{id}:{i}")
#         yield


# t1 = partial(task, 1, 100, 105)
# t2 = partial(task, 2, 30, 35)
# sched(t1, t2)


# # 七、 函数式编程
# # 迭代
# import functools
# import itertools

# x = map(lambda a, b: (a, b), [1, 2, 3], "abcd")
# print(list(x))
# # 聚合
# x = zip((1, 2, 3), "abcd", [1.1, 2.2])
# print(list(x))
# # 累积
# def calc(ret, x):
#     print(f"ret={ret}, x={x}")
#     return ret + x


# functools.reduce(calc, [1, 2, 3, 4, 5, 6])
# # 过滤
# x = filter(lambda n: n % 2 == 0, range(10))
# print(list(x))
# # 判断
# print(all([1, "a", ""]))
# print(any([1, "a", ""]))


# def count(n):
#     while True:
#         yield n
#         n += 1


# # 使用itertools才能对迭代器进行切片
# c = count(0)
# for x in itertools.islice(c, 10, 20):
#     print(x)


# 八、 展开嵌套的序列
from collections import Iterable


def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x


items = [1, 2, [3, 4, [5, 6], 7], 8]
# Produces 1 2 3 4 5 6 7 8
for x in flatten(items):
    print(x)
