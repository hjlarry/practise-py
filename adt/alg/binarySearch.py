def binarySearch(array, t):
    low = 0
    height = len(array) - 1
    while low <= height:
        mid = (low + height) // 2
        if array[mid] < t:
            low = mid + 1

        elif array[mid] > t:
            height = mid - 1

        else:
            return mid

    return -1


# 方法二
def binary_search_recursive(sorted_array, beg, end, val):
    if beg >= end:
        return False
    mid = int((beg + end) / 2)  # beg + (end-beg)/2
    if sorted_array[mid] == val:
        return mid
    elif sorted_array[mid] > val:
        return binary_search_recursive(
            sorted_array, beg, mid, val
        )  # 注意我依然假设 beg, end 区间是左闭右开的
    else:
        return binary_search_recursive(sorted_array, mid + 1, end, val)


def test_bin_search():
    a = [10, 30, 40, 70, 100, 120, 130, 190, 200]
    print(binary_search_recursive(a, 0, len(a), 200))
    assert binarySearch(a, 10) == 0
    assert binarySearch(a, 200) == 8
    assert binarySearch(a, 130) == 6
    assert binarySearch(a, 135) == -1

    assert binary_search_recursive(a, 0, len(a), 10) == 0
    assert binary_search_recursive(a, 0, len(a), 200) == 8
    assert binary_search_recursive(a, 0, len(a), 130) == 6
    assert binary_search_recursive(a, 0, len(a), 135) is False


if __name__ == "__main__":
    test_bin_search()
