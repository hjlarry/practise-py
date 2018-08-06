1. 写一个匹配URL的正则表达式

支持如 www.google.com、http://www.example/file.html https://douban.com/tag 等URL的匹配

2. 写一个匹配IP地址的正则表达式

支持如 192.168.0.1，8.8.8.8 等IP地址的匹配

3. 写3个正则表达式，完成下面三个例子：

- 把字符串 2018-01-01 用正则转化成 01/01/2018
- 实现一个函数，把 CamelCase 字符串 用正则转化成 camel_case
- 在slack中，存在uid和id的对应关系，如下面的变量 ID_NAMES 。通过Slack的API能获取聊天记录，但是内容用的是uid，请用正则表达式re.sub函数实现uid和id的转换
```
ID_NAMES = {'U1EAT8MG9': 'xiaoming', 'U0K1MF23Z': 'laolin'}

s = '<@U1EAT8MG9>, <@U0K1MF23Z> 嗯 确实是这样的'
```
提示:re.sub函数第二个参数是一个pattern，不仅可以是一个正则表达式，还可以是一个函数！

4. 实现Fibonacci函数

实现Fibonacci(斐波那契数列)函数fib:
```
>>> [fib(n) for n in range(16)]
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
```
提示：递归、缓存（标准库自带的缓存方案）

5. 实现PYTHON版本的TREE

在之前的学习中大家都见到我用tree命令，它以树状图列出目录的内容：
```
❯ tree -L 1
.
├── setup.py
├── token.pkl
├── venv
└── zhuanlan.py

1 directory, 3 files

~/test2 t*
❯ tree -L 2
.
├── setup.py
├── token.pkl
├── venv
│   ├── bin
│   ├── include
│   ├── lib
│   └── pip-selfcheck.json
└── zhuanlan.py
```
使用Python实现tree命令，只支持--help(显示帮助信息)和-L参数即可(如果不指定-L参数则打印该目录前所有深度的目录和文件)。下面是帮助信息的输出：
```
❯ python3 5.py --help
usage: 5.py [-h] [-L LEVEL] PATH

list contents of directories in a tree-like format.

positional arguments:
  PATH                  directory path name

optional arguments:
  -h, --help            show this help message and exit
  -L LEVEL, --level LEVEL
                        Descend only level directories deep.
```
提示：os、argparse模块，要忽略.开头的文件和目录

6. 写一个装饰器inject，在__init__时自动给类注入参数：
```
In : class Test:
...:     @injectArguments
...:     def __init__(self, x, y, z):
...:         pass
...:     
            
In : t = Test(x=4, y=5, z=6)

In : t.x, t.y, t.z
Out: (4, 5, 6)
```
提示：修改self.__dict__

7. 使用WITH写一个函数调用计时的上下文管理器
```
In : with Timed():
...:     sleep(2)
...:     
Cost: 2.0050339698791504
```
再改写一个调用计时的装饰器，提示，可以直接把一个with管理器转换成装饰器：
```
In : @Timed2()
...: def f():
...:     sleep(2)
...:     
         
In : f()
Cost: 2.000157356262207
```
提示：魔术方法 __enter__、__exit__，time模块、ContextDecorator

8. 实现一个类，可以完成链式调用
```
In : Seq(1, 2, 3, 4)\
...:     .map(lambda x: x * 2)\
...:     .filter(lambda x: x > 4)\
...:     .reduce(lambda x, y: x + y)
...: 
Out: 14
```
9. PYTHON读取超大文件

开放性题目，如果Python读取一个10G文件, 你觉得怎么样的方式更快，更省内存呢？

### 参考答案
