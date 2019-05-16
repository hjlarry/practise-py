import time
from myasync.tasks import sleep, schedule_task
from myasync.eventloop import get_event_loop

# https://zhuanlan.zhihu.com/p/64991670


def compute(x, y):
    print(f"compute:{x} + {y}")
    yield from sleep(1)
    return x + y


@schedule_task(3)
def print_sum(x, y):
    print(time.time())
    result = yield from compute(x, y)
    print(f"{x} + {y} = {result}")


loop = get_event_loop()
loop.run_not_complete(print_sum(1, 5))
