import itertools
from sudoku import print_answers


def is_full(challange, m=3):
    for i, j in itertools.product(range(m ** 2), repeat=2):
        if challange[i][j] is None:
            return False
    return True


def cal_candidate(challange, x, y, m=3):

    candidate = list(range(1, m ** 2 + 1))
    for i in range(m ** 2):
        # 确认一行没有重复数字
        if challange[x][i] in candidate:
            candidate.remove(challange[x][i])
        # 确认一列没有重复数字
        if challange[i][y] in candidate:
            candidate.remove(challange[i][y])
    # 确认一个区块(3*3)没有重复数字
    for i, j in itertools.product(range(m), repeat=2):
        # x0, y0 分别代表了空格所处区块的位置
        x0, y0 = x - x % m, y - y % m
        if challange[x0 + i][y0 + j] in candidate:
            candidate.remove(challange[x0 + i][y0 + j])
    return candidate


def least_candidate(challange, m=3):
    least, x, y = m ** 2, -1, -1
    for i, j in itertools.product(range(m ** 2), repeat=2):
        if not challange[i][j]:
            num = len(cal_candidate(challange, i, j))
            if num < least:
                least = num
                x, y = i, j
    return x, y


def solving_soduku(challange, m=3):
    # 如果数独列表已满，返回列表
    if is_full(challange):
        return challange

    # 找到填入数字最少的空格位置
    x, y = least_candidate(challange)

    # 为了方便递归，我们用id来表示每个空格
    id = x * (m ** 2) + y

    # try_candidate函数是我们的递归函数
    result = try_candidate(challange, id)
    return result


def try_candidate(challange, id, m=3):
    # 首先是基本结束条件
    if is_full(challange):
        return challange

    # 根据id解析出x,y轴坐标
    x = id // (m ** 2)
    y = id % (m ** 2)

    # 循环判断当前空格是否为None
    while challange[x][y]:
        # 注意,变量id可能越界
        # 所以需要取模运算来防止越界
        id = (id + 1) % m ** 4
        x = id // (m ** 2)
        y = id % (m ** 2)
    candidate = cal_candidate(challange, x, y)

    # 基本返回条件1
    if len(candidate) == 0:
        return False

    # 顺序选择数字
    # 并向下递归
    for i in range(len(candidate)):
        challange[x][y] = candidate[i]

        # 自身的数字填好了
        # 准备向下一个空格递归
        result_r = try_candidate(challange, (id + 1) % m ** 4)
        if not result_r:
            # 如果后面的空格
            # 返回None
            # 那么我们继续选择别的数
            pass
        else:
            # 后面的空格说OK!
            # 很好我们也说OK
            return challange

    # 注意，如果程序运行到了这一步
    # 说明没有合适的数字可以选择
    # 需要把自身恢复成初始状态
    # 即把空格中数字置为None
    challange[x][y] = None
    return False


testing = [
    [None, None, None, 3, None, 6, None, None, None],
    [None, 1, None, 8, None, None, None, None, 9],
    [5, 6, None, None, 4, None, 8, 3, None],
    [None, None, 8, None, None, None, None, 2, None],
    [None, None, None, 7, 6, None, None, None, None],
    [4, None, None, None, None, None, 5, None, None],
    [6, None, 2, 4, None, None, None, 9, 1],
    [None, None, None, None, 2, 9, None, None, None],
    [None, 8, None, None, 1, None, None, None, 6],
]
result = solving_soduku(testing)
print_answers(result)
