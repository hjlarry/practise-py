1. 写一个生成素数的迭代器, 能迭代小于某数值以下的素数

要求: 不要使用yield

```
# 写一个类 Prime
In : for i in Prime(30):
...:     print(i)
...:
2
3
5
7
11
13
17
19
23
29
```
2. 写一个生成素数的生成器, 但生成一定数量之后就会停止
```
In : p = prime(3)

In : next(p)
Out: 2

In : next(p)
Out: 3

In : next(p)
Out: 5

In : next(p)
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
<ipython-input-6-aa41e7f2fa96> in <module>()
----> 1 next(p)

StopIteration:

In : list(prime(5))
Out: [2, 3, 5, 7, 11]
```

3. 使用YIELD实现用轮转调度(ROUND-ROBIN):

轮转是一种很基础的调度算法，在业务不复杂时可以让业务逻辑达到一定的平衡

```
In : list(roundrobin('ABC', 'D', 'EF'))
Out: ['A', 'D', 'E', 'B', 'F', 'C']
```
提示：使用collections.deque/或者itertools


### 参考答案
https://talk.pycourses.com/topic/38/python%E5%85%A5%E9%97%A8-%E4%BD%9C%E4%B8%9A-%E4%B8%89-%E7%AD%94%E6%A1%88

