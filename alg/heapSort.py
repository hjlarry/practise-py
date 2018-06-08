from heap import MaxHeap


def heap_sort(arr):
    m = MaxHeap()
    result = []
    for i in arr:
        m.add(i)
    for _ in range(len(arr)):
        result.append(m.extract())
    return result


def test_heapsort_reverse():
    import random
    l = list(range(10))
    random.shuffle(l)
    assert heap_sort(l) == sorted(l, reverse=True)


test_heapsort_reverse()