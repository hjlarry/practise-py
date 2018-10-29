import gc

flags = (gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_SAVEALL) # 相当于DEBUG_LEAK
gc.set_debug(flags)

class Graph:
    def __init__(self, name):
        self.name = name
        self.next = None

    def set_next(self, next):
        self.next = next

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"


class CleanupGraph(Graph):
    def __del__(self):
        print(f"{self}.__del__()")


one = Graph('one')
two = Graph('two')
one.set_next(two)
two.set_next(one)

three = CleanupGraph('three')

four = CleanupGraph('four')
five = CleanupGraph('five')
four.set_next(five)
five.set_next(four)

# 删除引用
one = two = three = four = five = None
# 强制回收。
print('Collecting')
gc.collect()
print('done')
# 报告哪些被留下了
for o in gc.garbage:
    if isinstance(o, Graph):
        print(f'retained:{o} 0x{id(o)}')
# 重新设置 debug 标识，避免在退出时会有额外的信息导致例子混乱
gc.set_debug(0)
