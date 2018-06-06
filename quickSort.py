a = [30, 10, 40, 50, 25, 9, 7, 100]


def sort(arr, low=None, high=None):
    l = low if low else 0
    h = high if high else len(arr) - 1
    key = arr[l]
    if l >= h:
        return arr
    while l < h:
        while l < h and arr[h] >= key:
            h -= 1
        arr[l], arr[h] = arr[h], arr[l]
        while l < h and arr[l] <= key:
            l += 1
        arr[h], arr[l] = arr[l], arr[h]
        print(arr)
    arr[l] = key
    sort(arr, low, l - 1)
    sort(arr, h + 1, high)
    print(1)
    return arr


def sort2(arr):
    print(arr)
    if len(arr) < 2:
        return arr
    pivot = arr[0]
    less = []
    high = []
    for i in range(1, len(arr)):
        if arr[i] > pivot:
            high.append(arr[i])
        else:
            less.append(arr[i])
    return less, high


print(sort2(a))

dict
