import random


def bubbleSort(arr):
    for i in range(1, len(arr)):
        n = 0
        while n < len(arr) - i:
            if arr[n] > arr[n + 1]:
                arr[n], arr[n + 1] = arr[n + 1], arr[n]
            n += 1


def insertSort(arr):
    for i in range(1, len(arr)):
        value = arr[i]
        pos = i
        while pos > 0 and value < arr[pos - 1]:
            arr[pos] = arr[pos - 1]
            pos -= 1
        arr[pos] = value


def selectSort(arr):
    for i in range(1, len(arr)):
        posOfMax = 0
        n = 0
        lastElement = len(arr) - i
        while n <= lastElement:
            if arr[n] > arr[posOfMax]:
                posOfMax = n

            n += 1
        arr[posOfMax], arr[lastElement] = arr[lastElement], arr[posOfMax]


def test_sort(func):
    array = list(range(10))
    random.shuffle(array)
    sorted_arr = sorted(array)
    func(array)
    assert sorted_arr == array


if __name__ == "__main__":
    test_sort(bubbleSort)
    test_sort(insertSort)
    test_sort(selectSort)
