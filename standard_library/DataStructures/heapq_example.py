# python使用了最小堆
import math
import heapq
import random
from io import StringIO

data = [19, 9, 4, 10, 11]


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


heap = []
print("random:", data)
print()

for n in data:
    print(f"add {n:>3}")
    # 插入时按堆结构插入
    heapq.heappush(heap, n)
    # heap.append(n)
    show_tree(heap)
    print(heap)

data2 = data[:]
heapq.heapify(data2)
print(data2)
print(data)

show_tree(data2)
min_ = heapq.heappop(data2)
print("heap pop:", min_)
show_tree(data2)
min_ = heapq.heapreplace(data2, 12)
print("replaced:", min_)
show_tree(data2)
print()

print("all:", data)
print("3 largest:", heapq.nlargest(3, data))
print("3 smallest:", heapq.nsmallest(3, data))
print("after:", data)

# 高效合并多个已排序列表
# list(sorted(itertools.chain(*data))) 会占用大量内存
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
