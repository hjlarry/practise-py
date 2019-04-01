## Event, Lock, Condition, Semaphore, Pipe Example
import sys
import multiprocessing
import time
import random

print("***Event example:")


def wait_for_event(e):
    print("wait for event starting:")
    e.wait()
    print("wait_for_event, e.is_set() -->", e.is_set())


def wait_for_event_timeout(e, t):
    print("wait for event timeout starting:")
    e.wait(t)
    print("wait_for_event_timeout, e.is_set() -->", e.is_set())


e = multiprocessing.Event()
w1 = multiprocessing.Process(target=wait_for_event, args=(e,), name="block")
w1.start()
w2 = multiprocessing.Process(
    target=wait_for_event_timeout, args=(e, 2), name="non-block"
)
w2.start()
print("wait for call e is set:")
time.sleep(4)
e.set()
print("main event is set")
print()


print("***Lock example:")


def work_with(lock, stream):
    with lock:
        stream.write("lock acquied via with \n")


def work_not_with(lock, stream):
    lock.acquire()
    try:
        stream.write("lock acquied via directly \n")
    finally:
        lock.release()


lock = multiprocessing.Lock()
w = multiprocessing.Process(target=work_with, args=(lock, sys.stdout))
nw = multiprocessing.Process(target=work_not_with, args=(lock, sys.stdout))
w.start()
nw.start()
w.join()
nw.join()
print()


print("***Condition example:")


def stage_1(cond):
    name = multiprocessing.current_process().name
    print("Starting ", name)
    with cond:
        print(f"{name} done and ready for stage_2")
        cond.notify_all()


def stage_2(cond):
    name = multiprocessing.current_process().name
    print("Starting ", name)
    with cond:
        cond.wait()
        print(f"{name} running")


condition = multiprocessing.Condition()
s1 = multiprocessing.Process(target=stage_1, args=(condition,), name="s1")
s2_clients = [
    multiprocessing.Process(target=stage_2, args=(condition,), name=f"stage2[{i}]")
    for i in range(1, 3)
]
for c in s2_clients:
    c.start()
    time.sleep(1)
s1.start()
s1.join()
for c in s2_clients:
    c.join()
print()

print("***Semaphore example:")


class ActivePool:
    def __init__(self):
        self.mgr = multiprocessing.Manager()
        self.active = self.mgr.list()
        self.lock = multiprocessing.Lock()

    def make_active(self, name):
        with self.lock:
            self.active.append(name)

    def make_inactive(self, name):
        with self.lock:
            self.active.remove(name)

    def __str__(self):
        with self.lock:
            return str(self.active)


def worker(s, pool):
    name = multiprocessing.current_process().name
    with s:
        pool.make_active(name)
        print(f"Activating {name} now running {pool}")
        time.sleep(random.random())
        pool.make_inactive(name)


pool = ActivePool()
s = multiprocessing.Semaphore(3)
jobs = [
    multiprocessing.Process(target=worker, args=(s, pool), name=f"worker[{i}]")
    for i in range(10)
]
for j in jobs:
    j.start()

while True:
    alive = 0
    for j in jobs:
        if j.is_alive():
            alive += 1
            j.join(timeout=0.1)
            print("now running ", pool)
    if alive == 0:
        print("Done")
        break
print()

print("***Pipe example:")
# Pipe 性能是高于 Queue的
def producer1(pipe):
    pipe.send("hello larry")


def consumer1(pipe):
    print(pipe.recv())


receive_pipe, send_pipe = multiprocessing.Pipe()
p = multiprocessing.Process(target=producer1, args=(send_pipe,))
c = multiprocessing.Process(target=consumer1, args=(receive_pipe,))

c.start()
p.start()

c.join()
p.join()
