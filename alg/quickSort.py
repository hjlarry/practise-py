import random


# 额外空间快排
def quick_sort(arr):
    if len(arr) < 2:
        return arr

    pivot_index = 0
    pivot = arr[pivot_index]
    less = []
    high = []

    for i in arr[pivot_index + 1:]:
        if i > pivot:
            high.append(i)
        elif i < pivot:
            less.append(i)

    return quick_sort(less) + [pivot] + quick_sort(high)


# 原地快排，不占用额外空间
def inplace_sort(arr, low, high):
    if low < high:
        pivot_index = low
        l = pivot_index + 1
        h = high - 1
        while True:
            while l <= h and arr[l] < arr[pivot_index]:
                l += 1
            while l <= h and arr[h] >= arr[pivot_index]:
                h -= 1

            if l > h:
                break
            else:
                arr[h], arr[l] = arr[l], arr[h]
        arr[pivot_index], arr[h] = arr[h], arr[pivot_index]
        inplace_sort(arr, low, h)
        inplace_sort(arr, h + 1, high)


def test_quick_sort():
    arr = list(range(20))
    random.shuffle(arr)
    assert sorted(arr) == quick_sort(arr)


def test_inplace_sort():
    arr = list(range(20))
    random.shuffle(arr)
    sorted_arr = sorted(arr)
    inplace_sort(arr, 0, len(arr))
    assert sorted_arr == arr
