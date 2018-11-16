from concurrent import futures
import time


def task(n):
    time.sleep(n)
    print("task done ", n)
    return n / 10


ex = futures.ThreadPoolExecutor(max_workers=2)
# cancel取消任务，只能取消未开始执行的任务
f1 = ex.submit(task, 2)
f2 = ex.submit(task, 2)
f3 = ex.submit(task, 2)
print(f1.cancel())
print(f3.cancel())
print(f1.result())
print()

# wait 会阻塞等待传入的第一个参数的任务去执行， 而return_when默认是所有任务结束后则不阻塞
all_tasks = [ex.submit(task, i) for i in range(2, 5)]
futures.wait(all_tasks, return_when=futures.FIRST_COMPLETED)
print('wait start')
print()

# 回调
def task_callback(n):
    print(f"{n}: sleeping ")
    time.sleep(0.5)
    print(f"{n}: done ")
    return n ** 3


def done(fn):
    if fn.cancelled():
        print(f"{fn.arg}: cancelled")
    elif fn.done():
        error = fn.exception()
        if error:
            print(f"{fn.arg}: error returned:{error}")
        else:
            result = fn.result()
            print(f"{fn.arg}: value returned:{result}")


print("main starting")
f = ex.submit(task_callback, 5)
f.arg = 5
f.add_done_callback(done)
result = f.result()
print()

# 异常处理
def task_exec(n):
    print(f"{n} starting")
    raise ValueError(f"the value {n} is not good")


print("main starting")
f = ex.submit(task_exec, 5)
error = f.exception()
print("main error ", error)
try:
    result = f.result()
except ValueError as e:
    print("main saw error when accessing result ", e)
print()

# 上下文管理器
with futures.ThreadPoolExecutor(max_workers=2) as ex:
    print("main starting")
    ex.submit(task_callback, 1)
    ex.submit(task_callback, 2)
    ex.submit(task_callback, 3)
print("main done")
ex.shutdown()
