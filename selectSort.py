a = [30, 10, 40, 50, 25, 9, 7, 100]


def sort(arr):
    for i in range(1, len(arr)):
        posOfMax = 0
        n = 0
        lastElement = len(arr) - i
        while n <= lastElement:
            if arr[n] > arr[posOfMax]:
                posOfMax = n

            n += 1
        arr[posOfMax], arr[lastElement] = arr[lastElement], arr[posOfMax]
        print(arr)


sort(a)
