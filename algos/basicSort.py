import random


def bubble_sort(arr):
    for i in range(1, len(arr)):
        n = 0
        while n < len(arr) - i:
            if arr[n] > arr[n + 1]:
                arr[n], arr[n + 1] = arr[n + 1], arr[n]
            n += 1


def insert_sort(arr):
    for i in range(1, len(arr)):
        value = arr[i]  # 保存当前位置的值，因为转移的过程中它的值可能会被覆盖
        pos = i  # 定义位置，确保[0,i]有序的
        while pos > 0 and value < arr[pos - 1]:
            arr[pos] = arr[pos - 1]
            pos -= 1
        arr[pos] = value


def select_sort(arr):
    for i in range(1, len(arr)):
        posOfMax = 0  # 寻找最大元素的位置
        n = 0
        lastElement = len(arr) - i
        while n <= lastElement:
            if arr[n] > arr[posOfMax]:
                posOfMax = n
            n += 1
        arr[posOfMax], arr[lastElement] = arr[lastElement], arr[posOfMax]


def short_bubble_sort(arr):
    exchanges = True  # 短冒泡排序再检测一次列表遍历后没有交换元素，则表明已经排序成功，不再继续冒泡
    passnum = len(arr) - 1
    while passnum > 0 and exchanges:
        exchanges = False
        for n in range(passnum):
            if arr[n] > arr[n + 1]:
                exchanges = True
                arr[n], arr[n + 1] = arr[n + 1], arr[n]
        passnum -= 1


def test_sort(func):
    array = list(range(10))
    random.shuffle(array)  # 打乱数组是原地操作
    sorted_arr = sorted(array)  # 内置sorted会创建一个新的数组进行排序
    func(array)  # 我们的排序方法也都是原地操作
    assert sorted_arr == array


if __name__ == "__main__":
    test_sort(bubble_sort)
    test_sort(insert_sort)
    test_sort(select_sort)
    test_sort(short_bubble_sort)
