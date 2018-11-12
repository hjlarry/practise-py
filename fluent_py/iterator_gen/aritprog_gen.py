class ArithmeticProgression:
    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end

    def __iter__(self):
        result = type(self.begin + self.step)(self.begin)
        forever = self.end is None
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index
            # 不使用下面的累加方式可以降低处理浮点时累积效应致错的风险
            # result += self.step


ap = ArithmeticProgression(0, 1, 3)
print(list(ap))
ap = ArithmeticProgression(1, 0.5, 3)
print(list(ap))
ap = ArithmeticProgression(0, 1 / 3, 3)
print(list(ap))

# 函数版更简洁
def artiprog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index


import itertools


def artiprog_gen_v2(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen

ap = artiprog_gen_v2(0, 1, 3)
print(list(ap))
ap = artiprog_gen_v2(1, 0.5, 3)
print(list(ap))
ap = artiprog_gen_v2(0, 1 / 3, 3)
print(list(ap))