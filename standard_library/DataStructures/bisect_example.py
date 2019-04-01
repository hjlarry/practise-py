import bisect

# bisect模块主要是向列表中有序插入数据的
values = [14, 85, 77, 26, 50, 45, 66, 79, 10, 3, 84, 77, 1]

print("New  Pos  Contents")
print("---  ---  --------")

l = []
for i in values:
    position = bisect.bisect(l, i)
    bisect.insort(l, i)
    print(f"{i:3}  {position:3}", l)

print()
l = []
for i in values:
    position = bisect.bisect_left(l, i)
    bisect.insort_left(l, i)  # 结果相同，只是insort_left是将相同的值插入到左侧
    print(f"{i:3}  {position:3}", l)
