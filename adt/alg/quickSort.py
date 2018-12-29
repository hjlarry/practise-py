import random


def quick_sort(arr):
    """额外空间快排"""
    if len(arr) < 2:  # 递归出口
        return arr

    pivot_index = 0
    pivot = arr[pivot_index]
    less_part = []
    great_part = []

    for i in arr[pivot_index + 1 :]:
        if i > pivot:
            great_part.append(i)
        elif i < pivot:
            less_part.append(i)

    return quick_sort(less_part) + [pivot] + quick_sort(great_part)


def inplace_quick_sort(arr, begin, end):
    """原地快排，不占用额外空间"""
    if begin < end:
        pivot_index = partition(arr, begin, end)
        inplace_quick_sort(arr, begin, pivot_index)
        inplace_quick_sort(arr, pivot_index + 1, end)


def partition(arr, begin, end):
    pivot_index = begin
    pivot = arr[pivot_index]
    left = pivot_index + 1
    right = end - 1
    while True:
        # 从左边去找比基准点大的，右边去找比基准点小的，交换其位置
        while left <= right and arr[left] < pivot:
            left += 1
        while right >= left and arr[right] >= pivot:
            right -= 1

        if left > right:
            break
        else:
            arr[left], arr[right] = arr[right], arr[left]
    # 交换基准点至交叉点
    arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
    return right  # 新的基准点位置


def nth_element(arr, begin, end, nth):
    """查找一个数组第N小的元素"""
    if begin < end:
        pivot_index = partition(arr, begin, end)
        if pivot_index > nth - 1:
            return nth_element(arr, begin, pivot_index, nth)
        elif pivot_index < nth - 1:
            return nth_element(arr, pivot_index + 1, end, nth)
        else:
            return arr[pivot_index]


def test_quick_sort():
    arr = list(range(20))
    random.shuffle(arr)
    assert sorted(arr) == quick_sort(arr)


def test_inplace_sort():
    arr = list(range(20))
    random.shuffle(arr)
    sorted_arr = sorted(arr)
    inplace_quick_sort(arr, 0, len(arr))
    assert sorted_arr == arr


def test_nth():
    arr = list(range(10))
    random.shuffle(arr)
    assert nth_element(arr, 0, len(arr), 3) == 2


if __name__ == "__main__":
    test_quick_sort()
    test_inplace_sort()
    test_nth()
