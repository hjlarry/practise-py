"""
线程池的意义：
1. 有时我们不止需要去限制同时进行的任务数量，还需要得到线程/任务的状态以及返回值
2. 当一个线程工作完成时主线程能立即知道
3. 让多进程多线程的接口编码一致
"""


from concurrent import futures
import time


def task(n):
    time.sleep(n)
    return n / 10


ex = futures.ThreadPoolExecutor(max_workers=2)
f = ex.submit(task, 2)
print("main:future:", f)
print("is task finish?", f.done())
print("main:waiting for real results")
# 获取result时会阻塞
real_res = f.result()
print("main:real results", real_res)
print("main:future after results", f)
print("is task finish?", f.done())
print()

# for批量提交至线程池，as_completed实际上是生成器函数，产生任务运行结果了会立即返回
wait_for = [ex.submit(task, i) for i in range(5, 0, -1)]
for f in futures.as_completed(wait_for):
    print("main results :", f.result())
print()

# map批量提交至线程池，会直接得到结果并对应好提交的func的顺序一起返回
results = ex.map(task, range(5, 0, -1))
print("main:unprocessed results", results)
print("main:waiting for real results")
real_res = list(results)
print("main:real results", real_res)
ex.shutdown()
print()

"""
submit+as_complete 会比 map 更加灵活：
1. 因为map只能处理参数不同的同一个可调用对象，而submit可以是不同调用对象
2. map返回的是生成器，因其结果按顺序返回，for循环遍历时，如果第一个调用10秒，
其他调用1秒，则会先阻塞10秒其他不阻塞顺序返回，而as_complete则可以有了结果就返回
"""
