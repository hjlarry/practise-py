a = [30, 10, 40, 50, 25, 9, 7, 100]


def sort(arr):
    for i in range(1, len(arr)):
        n = 0
        while n < len(arr) - i:
            if arr[n] > arr[n + 1]:
                arr[n], arr[n + 1] = arr[n + 1], arr[n]
            n += 1
        print(arr)


sort(a)


# 短冒泡排序再检测一次列表遍历后没有交换元素，则表明已经排序成功，不再继续冒泡
def shortBubbleSort(arr):
    exchanges = True
    passnum = len(arr) - 1

    while passnum > 0 and exchanges:
        exchanges = False
        for n in range(passnum):
            if arr[n] > arr[n + 1]:
                exchanges = True
                arr[n], arr[n + 1] = arr[n + 1], arr[n]
        print(arr)
        passnum -= 1


# shortBubbleSort(a)
shortBubbleSort([10, 20, 30, 110, 40, 50, 60, 70, 80, 90])
sort([10, 20, 30, 100, 40, 50, 60, 70, 80, 90])
