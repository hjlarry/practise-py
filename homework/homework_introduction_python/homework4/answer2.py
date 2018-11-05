import multiprocessing
import random
import time

tasks_queue = multiprocessing.JoinableQueue()
event = multiprocessing.Event()


def re_num(n):
    return n


def consumer1(in_queue, event):
    while 1:
        if event.is_set():
            f, args = in_queue.get()
            res = f(args)
            print(f'Consumer1: {res}')


def consumer2(in_queue, event):
    while 1:
        if not event.is_set():
            f, args = in_queue.get()
            res = f(args)
            print(f'Consumer2: {res}')


def producer(in_queue, event):
    n = 0
    while 1:
        x = random.randint(1, 100)
        in_queue.put((re_num, x))
        print(f'Produce: {x}')
        n += 1
        if n > 5:
            event.set()
        time.sleep(random.random())
        if x > 95:
            break


processes = []
p0 = multiprocessing.Process(target=producer, args=(tasks_queue, event))
p0.start()
processes.append(p0)

p1 = multiprocessing.Process(target=consumer1, args=(tasks_queue, event))
p1.start()
processes.append(p1)

p2 = multiprocessing.Process(target=consumer2, args=(tasks_queue, event))
p2.start()
processes.append(p2)

tasks_queue.join()
for p in processes:
    p.join()