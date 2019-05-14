from myasync.tasks import sleep
from myasync.eventloop import get_event_loop

# https://zhuanlan.zhihu.com/p/64991670


def compute(x, y):
    yield from sleep(1)
    return x + y


def print_sum(x, y):
    result = yield from compute(x, y)
    print("%s + %s = %s" % (x, y, result))


loop = get_event_loop()
loop.run_until_complete(print_sum(1, 2))
