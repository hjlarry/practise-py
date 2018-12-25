import time


class BitMap:
    def __init__(self, max=90):
        # 因为单个整型只能使用31位，所以需要的位数除以31并向上取整则可得知需要几个数组元素
        self.size = self.calcElementIndex(max, up=True)
        self.data = [0 for _ in range(self.size)]

    def calcElementIndex(self, num, up=False):
        # 计算数字在数组中的索引，up 为向上取整
        if up:
            return int((num + 31 - 1) // 31)
        return num // 31

    def calcBitIndex(self, num):
        # 计算数字在位中的索引
        return num % 31

    def set(self, i):
        # 置1操作
        ele_index = self.calcElementIndex(i)
        bit_index = self.calcBitIndex(i)
        elem = self.data[ele_index]
        self.data[ele_index] = elem | (1 << bit_index)

    def clean(self, i):
        # 清0操作
        ele_index = self.calcElementIndex(i)
        bit_index = self.calcBitIndex(i)
        elem = self.data[ele_index]
        self.data[ele_index] = elem & (~(1 << bit_index))

    def is_set(self, i):
        # 是否有值
        ele_index = self.calcElementIndex(i)
        bit_index = self.calcBitIndex(i)
        if self.data[ele_index] & (1 << bit_index):
            return True
        return False


bitmap = BitMap(87)
bitmap.set(10)
bitmap.set(34)
bitmap.set(50)
print(bitmap.data)
bitmap.clean(50)
print(bitmap.data)


t1 = time.time()

MAX = 10000000
suffle_array = [45, 2, 78, 35, 67, 90, 879, 0, 340, 123, 46]
bitmap = BitMap(MAX)
for num in suffle_array:
    bitmap.set(num)

result = [i for i in range(MAX + 1) if bitmap.is_set(i)]

print(result)
print(time.time() - t1)
