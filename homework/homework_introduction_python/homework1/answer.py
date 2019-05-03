"""
参考答案
https://talk.pycourses.com/topic/15/python%E5%85%A5%E9%97%A8-%E4%BD%9C%E4%B8%9A-%E4%B8%80-%E7%AD%94%E6%A1%88/21


1. 乘法口诀表
要求：编写一个程序，执行时输出乘法口诀表:
```
❯ python 1.py
1*1=1	
1*2=2	2*2=4	
1*3=3	2*3=6	3*3=9	
1*4=4	2*4=8	3*4=12	4*4=16	
1*5=5	2*5=10	3*5=15	4*5=20	5*5=25	
1*6=6	2*6=12	3*6=18	4*6=24	5*6=30	6*6=36	
1*7=7	2*7=14	3*7=21	4*7=28	5*7=35	6*7=42	7*7=49	
1*8=8	2*8=16	3*8=24	4*8=32	5*8=40	6*8=48	7*8=56	8*8=64	
1*9=9	2*9=18	3*9=27	4*9=36	5*9=45	6*9=54	7*9=63	8*9=72	9*9=81
```
"""
print("一、 乘法表")
for i in range(1, 10):
    for z in range(1, i + 1):
        print(f"{z}*{i}={i * z}", end=" ")
    print()
print()
"""
2. 列表去重

要求：编写一个函数，可以去除一个列表中重复的元素，并且保持元素的顺序：

```
In  : l = [1, 3, 6, 9, 3, 4, 1, 3]                                                                             
In  : unique(l)
Out: [1, 3, 6, 9, 4]
```
"""
from collections import OrderedDict


def unique(l):
    results = OrderedDict().fromkeys(l)
    return list(results.keys())


print("二、 列表去重")
print(unique([1, 3, 6, 9, 3, 4, 1, 3]))
print()

"""
3. 列表排序

现在有2个列表：
```
In : A = [1, 3, 7, 10, 5, 2]

In : B = [2, 3, 5]
```
B 是 A 的子集，但顺序是乱的，编写一个函数用 A 中的元素顺序对 B 排序:
```
In  : my_sort(A, B)
Out: [3, 5, 2]
```
"""


def mysort(A: list, B: list):
    return sorted(B, key=lambda x: A.index(x))


print("三、 列表排序")
A = [1, 3, 7, 10, 5, 2]
B = [2, 3, 5]
print(mysort(A, B))
print()

"""
4\. FIZZBUZZ
遍历并打印1到20，如果数字能被3整除，显示Fizz；如果数字能被5整除，显示Buzz；如果能同时被3和5整除，就显示FizzBuzz：

```
❯ python 4.py
1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz 16 17 Fizz 19 Buzz
```
"""


def fizzbuzz():
    for i in range(1, 21):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz", end=" ")
        elif i % 3 == 0:
            print("Fizz", end=" ")
        elif i % 5 == 0:
            print("Buzz", end=" ")
        else:
            print(i, end=" ")


print("四、 FIZZBUZZ")
print(fizzbuzz())
print()


def _not_divisible(n):
    return lambda x: x % n > 0


def primes():
    it = (x for x in range(2, 101))
    while True:
        n = next(it)
        yield n
        it = filter(_not_divisible(n), it)


print("五、 编写过滤1-100中的素数的函数")
print([n for n in primes()])
