"""
线程运行的两种方式分别为方法、继承 Thread 类
GIL的释放，解释器是依据字节码行数或时间片的以及IO操作的，它并不能解决线程间同步数据的问题
Python 的list,dict等都是线程安全的，它们有「原子操作」，GIL会保护这样的内部数据结构在更新时线程不会被释放。其他的数据结构如整数浮点数则不会受此保护
"""

import threading
import time
import logging


def worker(num):
    """thread worker function"""
    print(f"Worker {num}")
    print(threading.current_thread().getName())


threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()


class MyThread(threading.Thread):
    def run(self):  # 重写run方法，没有运行target
        logging.debug("this running")
        logging.debug(self._args)


for i in range(5):
    t = MyThread(target=worker, args=("dss", "asa"))
    t.start()


# Timer 提供了一个继承 Thread 的例子，也包含在 threading 模块中。Timer 在延迟一段时间后启动工作，他可以在延迟的这段时间内任何时间点取消。
def delayed():
    logging.debug("worker running")


t1 = threading.Timer(0.3, delayed)
t2 = threading.Timer(0.3, delayed)
t1.setName("t1")
t2.setName("t2")
logging.debug("starting timers")
t1.start()
t2.start()

logging.debug("waiting before canceling %s", t2.getName())
time.sleep(0.2)
logging.debug("canceling %s", t2.getName())
t2.cancel()  # 在delay参数内可以取消执行
logging.debug("done")

#%% [markdown]
# ## 线程同步

#%%
def wait_for_event(e):
    logging.debug("wait_for_event starting")
    event_is_set = e.wait()
    logging.debug("event set: %s", event_is_set)


def wait_for_event_timeout(e, t):
    while not e.is_set():
        logging.debug("wait_for_event_timeout starting")
        event_is_set = e.wait(t)
        logging.debug("event set: %s", event_is_set)
        if event_is_set:
            logging.debug("processing event")
        else:
            logging.debug("doing other work")


#%%
e = threading.Event()
t1 = threading.Thread(name="block", target=wait_for_event, args=(e,))
t2 = threading.Thread(name="nonblock", target=wait_for_event_timeout, args=(e, 2))
t1.start()
t2.start()
logging.debug("Waiting before calling event.set()")
time.sleep(0.3)
e.set()
logging.debug("Event is set")

#%% [markdown]
# wait() 方法可以接收一个参数，表示事件等待的超时时间


#%%


#%% [markdown]
# 除了使用 Events，另一种同步线程的方法是使用 Condition 对象。 Condition 使用了 Lock，所以它会绑定共享的资源，也就会让多个线程等待资源更新完成。
#
# 屏障」（Barrier）是另一种线程同步的机制。每个 Barrier 会建立起一个控制点，所有处在其中的线程都会被阻塞，直到所有的线程都到达这个控制点。它会让所有的线程单独启动，然后在它们全都准备好执行下一步前先阻塞住。

#%%
def worker(barrier):
    print(
        threading.current_thread().name,
        f"wait for barrier with {barrier.n_waiting} others",
    )
    worker_id = barrier.wait()
    print(f"{threading.current_thread().name} after barrier  {worker_id}")


NUM_T = 3
barrier = threading.Barrier(NUM_T)
threads = [
    threading.Thread(name=f"worker-{i}", target=worker, args=(barrier,))
    for i in range(NUM_T)
]
for t in threads:
    print(t.name, "starting")
    t.start()
    time.sleep(0.1)

for t in threads:
    t.join()


#%%
def worker(barrier):
    print(
        threading.current_thread().name,
        f"wait for barrier with {barrier.n_waiting} others",
    )
    try:
        worker_id = barrier.wait()
    except threading.BrokenBarrierError:
        print(f"{threading.current_thread().name} aborting")
    else:
        print(f"{threading.current_thread().name} after barrier  {worker_id}")


NUM_T = 3
barrier = threading.Barrier(NUM_T + 1)
threads = [
    threading.Thread(name=f"worker-{i}", target=worker, args=(barrier,))
    for i in range(NUM_T)
]
for t in threads:
    print(t.name, "starting")
    t.start()
    time.sleep(0.1)
barrier.abort()
for t in threads:
    t.join()

#%% [markdown]
# Barrier 的 abort() 方法会导致所有等待中的线程接收到一个 BrokenBarrierError。 我们可以使用此方法来告知那些被阻塞住的线程该结束了。这次我们将 Barrier 设置成比实际开始的线程多一个，这样所有的线程就会被阻塞住，我们调用 abort() 就可以引起 BrokenBarrierError 了。

#%%
class ActivePool:
    def __init__(self):
        self.active = []
        self.lock = threading.Lock()

    def make_active(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug(f"Running {self.active}")

    def make_inactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug(f"Running {self.active}")


def worker(s, pool):
    logging.debug("Wait for join the pool")
    with s:
        name = threading.current_thread().getName()
        pool.make_active(name)
        time.sleep(1)
        pool.make_inactive(name)


pool = ActivePool()
s = threading.Semaphore(2)

for i in range(4):
    t = threading.Thread(target=worker, name=str(i), args=(s, pool))
    t.start()


#%% [markdown]
# 有时我们需要允许多个工作函数在同一时间访问同一个资源，但我们也要限制可访问的总数。
# ActivePool 类只是用来追踪给定时刻下哪些线程在工作的。如果是实际情况中，资源池一般还要分配连接或者其他值给新的活动线程，并且当线程结束后回收这些值。
#
# ## thread local

#%%
import random


def show_value(data):
    try:
        val = data.value
    except AttributeError:
        logging.debug("Not value yet")
    else:
        logging.debug("value=%s", val)


def worker(data):
    show_value(data)
    data.value = random.randint(1, 100)
    show_value(data)


local_data = threading.local()
show_value(local_data)
local_data.value = 1000
show_value(local_data)

for i in range(2):
    t = threading.Thread(target=worker, args=(local_data,))
    t.start()

#%% [markdown]
# local() 类可以在每个线程中创建一个用于隐藏值的对象容器。 local_data.value 在当前的线程设置任何值前，对于当前线程来说它都什么都没有。

#%%
class MyLocal(threading.local):
    def __init__(self, value):
        super().__init__()
        logging.debug("Initializing %r", self)
        self.value = value


local_data = MyLocal(1000)
show_value(local_data)

for i in range(2):
    t = threading.Thread(target=worker, args=(local_data,))
    t.start()

