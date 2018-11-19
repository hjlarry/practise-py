"""
io密集型操作，多线程更快主要是由于线程切换相对于系统来说更容易，开销更小
"""

from concurrent import futures
import time


def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)


# ThreadPoolExecutor运行37秒, ProcessPoolExecutor运行 11秒, pypy运行ProcessPoolExecutor只需2.4秒, ThreadPoolExecutor只需2.5秒
with futures.ThreadPoolExecutor(max_workers=7) as ex:
    tasks = [ex.submit(fib, (i)) for i in range(25, 40)]
    start = time.time()
    for future in futures.as_completed(tasks):
        print("exe result:", future.result())
    print("use time:", time.time() - start)

