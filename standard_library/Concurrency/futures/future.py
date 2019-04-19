from concurrent import futures
import time


def task(n):
    time.sleep(n)
    print("task done ", n)
    return n / 10


print("一、 future.cancel()示例")
ex = futures.ThreadPoolExecutor(max_workers=2)
# cancel取消任务，只能取消未开始执行的任务
f1 = ex.submit(task, 2)
f2 = ex.submit(task, 2)
f3 = ex.submit(task, 2)
print(f1.cancel())
print(f3.cancel())
print(f1.result())
print()

print("二、 future.wait()示例")
# wait 会阻塞等待传入的第一个参数的任务去执行， 而return_when默认是所有任务结束后则不阻塞
all_tasks = [ex.submit(task, i) for i in range(2, 5)]
futures.wait(all_tasks, return_when=futures.FIRST_COMPLETED)
print("wait start")
print()
time.sleep(10)

print()
print("三、 future.add_done_callback()示例")
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


def done_test_callback(future):
    print(future)
    return 222


print("task_callback example starting")
f = ex.submit(task_callback, 5)
f.arg = 5
# add_done_callback传入的方法必须是一个以Future对象为参数的方法
f.add_done_callback(done_test_callback)
result = f.result()
print()


print("四、 future.exception()示例")
# 异常处理
def task_exec(n):
    print(f"{n} starting")
    raise ValueError(f"the value {n} is not good")


print("task_exec example starting")
f = ex.submit(task_exec, 5)
error = f.exception()
print("task_exec error ", error)
try:
    result = f.result()
except ValueError as e:
    print("main saw error when accessing result ", e)
print()

print("五、 上下文管理器示例")
# 上下文管理器
with futures.ThreadPoolExecutor(max_workers=2) as ex:
    print("context manager main starting")
    ex.submit(task_callback, 1)
    ex.submit(task_callback, 2)
    ex.submit(task_callback, 3)
print("main done")
ex.shutdown()
