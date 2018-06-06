def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        mid = len(arr) // 2
        left_half = merge_sort(arr[:mid])
        right_half = merge_sort(arr[mid:])
        return merge_sorted_list(left_half, right_half)


def merge_sorted_list(arr1, arr2):
    a , b = 0, 0
    a_max , b_max = len(arr1), len(arr2)
    new_arr = []

    while a < a_max and b < b_max:
        if arr1[a] < arr2[b]:
            new_arr.append(arr1[a])
            a += 1
        else:
            new_arr.append(arr2[b])
            b += 1

    if a == a_max:
        new_arr.extend(arr2[b:])
    elif b == b_max:
        new_arr.extend(arr1[a:])

    return new_arr


def test_merge_sort():
    import random
    seq = list(range(10))
    random.shuffle(seq)
    assert merge_sort(seq) == sorted(seq)