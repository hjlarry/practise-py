def binary_search(sorted_array, value):
    low = 0
    high = len(sorted_array) - 1
    while low <= high:
        # mid = (high + low) // 2  可能造成整数太大溢出
        # mid = low + ((high-low)>>1) 位运算会更快
        mid = low + (high - low) // 2
        if sorted_array[mid] < value:
            low = mid + 1

        elif sorted_array[mid] > value:
            high = mid - 1

        else:
            return mid

    return -1


# 方法二
def binary_search_recursive(sorted_array, begin, end, value):
    if begin >= end:
        return False
    mid = int((begin + end) / 2)  # beg + (end-beg)/2
    if sorted_array[mid] == value:
        return mid
    elif sorted_array[mid] > value:
        return binary_search_recursive(
            sorted_array, begin, mid, value
        )  # 注意我依然假设 beg, end 区间是左闭右开的
    else:
        return binary_search_recursive(sorted_array, mid + 1, end, value)


# 变形问题： 查找第一个值等于给定值的元素
def binary_search1(sorted_array, value):
    low = 0
    high = len(sorted_array) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if sorted_array[mid] < value:
            low = mid + 1

        elif sorted_array[mid] > value:
            high = mid - 1

        else:
            if mid == 0 or sorted_array[mid - 1] != value:
                return mid
            else:
                high = mid - 1

    return -1


# 变形问题： 查找最后一个值等于给定值的元素
def binary_search2(sorted_array, value):
    low = 0
    high = len(sorted_array) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if sorted_array[mid] < value:
            low = mid + 1

        elif sorted_array[mid] > value:
            high = mid - 1

        else:
            if mid == len(sorted_array) - 1 or sorted_array[mid + 1] != value:
                return mid
            else:
                low = mid + 1

    return -1


# 变形问题： 查找第一个大于等于给定值的元素
def binary_search3(sorted_array, value):
    low = 0
    high = len(sorted_array) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if sorted_array[mid] >= value:
            if mid == 0 or sorted_array[mid - 1] < value:
                return mid
            else:
                high = mid - 1
        else:
            low = mid + 1

    return -1


# 变形问题： 查找最后一个小于等于给定值的元素
def binary_search4(sorted_array, value):
    low = 0
    high = len(sorted_array) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if sorted_array[mid] <= value:
            if mid == len(sorted_array) - 1 or sorted_array[mid + 1] > value:
                return mid
            else:
                low = mid + 1
        else:
            high = mid - 1

    return -1


def test_bin_search():
    a = [10, 30, 40, 70, 100, 120, 130, 190, 200]
    print(binary_search_recursive(a, 0, len(a), 200))
    assert binary_search(a, 10) == 0
    assert binary_search(a, 200) == 8
    assert binary_search(a, 130) == 6
    assert binary_search(a, 135) == -1

    assert binary_search_recursive(a, 0, len(a), 10) == 0
    assert binary_search_recursive(a, 0, len(a), 200) == 8
    assert binary_search_recursive(a, 0, len(a), 130) == 6
    assert binary_search_recursive(a, 0, len(a), 135) is False

    b = [1, 3, 4, 5, 6, 8, 8, 8, 11, 18]
    assert binary_search1(b, 8) == 5
    assert binary_search2(b, 8) == 7
    assert binary_search3(b, 7) == 5
    assert binary_search4(b, 10) == 7


if __name__ == "__main__":
    test_bin_search()
