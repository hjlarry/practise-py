import random
import itertools
from copy import deepcopy


def make_board(m=3):
    # 默认数独的每一个区块是3 * 3的
    numbers = list(range(1, m ** 2 + 1))
    # 这里我们创建了一个含有所有可能出现数的列表（1~9）

    board = None
    # board是我们的数独二维列表
    while board is None:
        board = attempt_board(m, numbers)
    return board


def attempt_board(m, numbers):
    n = m ** 2

    board = [[None for _ in range(n)] for _ in range(n)]

    for i, j in itertools.product(range(n), repeat=2):
        # i,j分别代表的是我们的行和列
        # i0和j0代表的是board[i][j]所在的区块的起始位置
        i0, j0 = i - i % m, j - j % m

        random.shuffle(numbers)
        for x in numbers:
            # 分别检查行，列，区块
            if (
                x not in board[i]
                and all(row[j] != x for row in board)
                and all(x not in row[j0 : j0 + m] for row in board[i0:i])
            ):

                # 如果检查没有问题，就开始赋值
                board[i][j] = x
                break
        # 注意这个else的位置，是for...else...的语法结构
        else:
            return None
    return board


def print_board(board, m=3):
    numbers = list(range(1, m ** 2 + 1))

    # 每一行随机把5个数字变成None
    omit = 5  # omit变量掌控着每一行被抹去的数字个数
    challange = deepcopy(board)
    for i, j in itertools.product(range(omit), range(m ** 2)):
        x = random.choice(numbers) - 1
        challange[x][j] = None

    # 打印出整个数独列表
    spacer = "++-----+-----+-----++-----+-----+-----++-----+-----+-----++"
    print(spacer.replace("-", "="))
    for i, line in enumerate(challange):
        print(
            "||  {}  |  {}  |  {}  ||  {}  |  {}  |  {}  ||  {}  |  {}  |  {}  ||".format(
                *(cell or " " for cell in line)
            )
        )
        if (i + 1) % 3 == 0:
            print(spacer.replace("-", "="))
        else:
            print(spacer)
    return challange


def print_answers(board):
    spacer = "++-----+-----+-----++-----+-----+-----++-----+-----+-----++"
    print(spacer.replace("-", "="))
    for i, line in enumerate(board):
        print(
            "||  {}  |  {}  |  {}  ||  {}  |  {}  |  {}  ||  {}  |  {}  |  {}  ||".format(
                *(cell or " " for cell in line)
            )
        )
        if (i + 1) % 3 == 0:
            print(spacer.replace("-", "="))
        else:
            print(spacer)


if __name__ == "__main__":
    board = make_board()
    print_board(board)
    print_answers(board)
