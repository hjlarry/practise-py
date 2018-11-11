# 生成器函数代替SentenceIterator类
class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = text.split()

    def __iter__(self):
        # 观察UserList源码，其继承的Sequence基类实际上就是用了yield去实现
        return iter(self.words)
        # for word in self.words:
        #     yield word


s = Sentence("hello world haha")

for word in s:
    print(word)


# 对于解释器来说，所有的stackframe是分配在堆内存上的，
# gen_func.gi_frame.f_lasti保存了上次运行的结果，gen_func.gi_frame.f_locals保存了上下文字典
def gen_func():
    yield "aaa"
    name = "hejl"
    yield "bbb"
    age = 30
    yield "ccc"
    yield name, age


gen = gen_func()

import dis

dis.dis(gen)
print(gen.gi_frame.f_lasti, gen.gi_frame.f_back, gen.gi_frame.f_locals)
next(gen)
print(gen.gi_frame.f_lasti, gen.gi_frame.f_back, gen.gi_frame.f_locals)
next(gen)
print(gen.gi_frame.f_lasti, gen.gi_frame.f_back, gen.gi_frame.f_locals)

