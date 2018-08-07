from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import queue

q = queue.Queue()


def producer():
    for n in range(25, 35):
        q.put((fib, n))


def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)


t = threading.Thread(target=producer)
t.start()
executor = ThreadPoolExecutor(max_workers=3)
future_to_num = {}
while not q.empty():
    func, arg = q.get()
    future_to_num[executor.submit(func, arg)] = arg

for future in as_completed(future_to_num):
    num = future_to_num[future]
    try:
        result = future.result()
    except Exception as e:
        print(f'raise an exception: {e}')
    else:
        print(f'fib({num}) = {result}')