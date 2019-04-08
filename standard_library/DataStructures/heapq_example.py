# python使用了最小堆
import math
import heapq
import random
from io import StringIO


def show_tree(tree, total_width=36, fill=" "):
    output = StringIO()
    last_row = -1
    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i + 1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write("\n")
        columns = 2 ** row
        col_width = int(math.floor(total_width / columns))
        output.write(str(n).center(col_width, fill))
        last_row = row
    print(output.getvalue())
    print("-" * total_width)
    print()


print("一、堆插入数据示例：")
data = [19, 9, 4, 10, 11]
heap = []
print("random:", data)
for n in data:
    print(f"add {n:>3}")
    # 插入时按堆结构插入
    heapq.heappush(heap, n)
    # heap.append(n)
    show_tree(heap)
    print("插入堆数组后:", heap)
print()


print("二、堆排序示例：")
data2 = data[:]
heapq.heapify(data2)
print("排序后数组:", data2)
print("原数组:", data)
print()


print("三、取出和替换堆顶元素：")
show_tree(data2)
min_ = heapq.heappop(data2)
print("heap pop:", min_)
show_tree(data2)
min_ = heapq.heapreplace(data2, 12)
print("replaced:", min_)
show_tree(data2)
print()


# 当N的大小和要查找的集合大小相近时，那么先排序再切片会更快 sorted(items)[:N]
print("四、查找N个最大或最小元素：")
print("all:", data)
print("3 largest:", heapq.nlargest(3, data))
print("3 smallest:", heapq.nsmallest(3, data))
print("after:", data)
portfolio = [
    {"name": "IBM", "shares": 100, "price": 91.1},
    {"name": "AAPL", "shares": 50, "price": 543.22},
    {"name": "FB", "shares": 200, "price": 21.09},
    {"name": "HPQ", "shares": 35, "price": 31.75},
    {"name": "YHOO", "shares": 45, "price": 16.35},
    {"name": "ACME", "shares": 75, "price": 115.65},
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s["price"])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s["price"])
print(cheap)
print()


# list(sorted(itertools.chain(*data))) 会占用大量内存
print("五、使用堆高效合并多个已排序列表：")
random.seed(2016)
data = []
for i in range(4):
    new_data = list(random.sample(range(1, 101), 5))
    new_data.sort()
    data.append(new_data)
for i, d in enumerate(data):
    print(f"{i}:{d}")
print("Merged:")
for i in heapq.merge(*data):
    print(i, end=" ")
