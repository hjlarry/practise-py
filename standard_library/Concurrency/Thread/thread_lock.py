"""
A.锁的获取和释放会有一定的开销造成性能上的损耗
B.有可能造成两种死锁情况：
1. 同一个线程调用两次lock.acquire()而中间没有释放
2. 线程A(a,b),lock.acquire(a),lock.acquire(b)线程B(a,b),lock.acquire(b),lock.acquire(a)
C. 为解决情况一，尤其是函数调用子函数而导致的子函数锁不易被发觉，可使用可重入锁RLock
"""
import random
import threading
import logging
import time


class Counter:
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start

    def increment(self):
        logging.debug("Waiting for lock")
        self.lock.acquire()
        try:
            logging.debug("Lock acquired")
            self.value = self.value + 1  # 获取锁后对值操作，保证多个线程同时修改其内部状态不会出问题
        finally:
            self.lock.release()


def worker(c):
    for i in range(2):
        pause = random.random()
        logging.debug("Sleeping %0.02f", pause)
        time.sleep(pause)
        c.increment()
    logging.debug("Done")


logging.basicConfig(
    level=logging.DEBUG, format="[%(levelname)s] (%(threadName)-10s) %(message)s"
)
logging.info("一、 锁的使用")
counter = Counter()
for i in range(2):
    t = threading.Thread(target=worker, args=(counter,), name=str(i))
    t.start()

logging.debug("Waiting for work threads")
for t in threading.enumerate():
    # 这里只将工作的线程去阻塞执行了
    if t.getName() == str(0) or t.getName() == str(1):
        t.join()
logging.debug("Count value %d", counter.value)
time.sleep(1)

# 下个例子中，do_sth() 会尝试获得三次锁，并计算总共尝试了几次才获得这三次锁。
# 同时，lock_holder() 的循环会不断获取并释放锁，每次都有一小段间隔来模拟「正在加载...」。
def lock_holder(lock):
    logging.debug("Starting")
    while True:
        lock.acquire()
        try:
            logging.debug("Holding")
            time.sleep(1)
        finally:
            logging.debug("Not holding")
            lock.release()
        time.sleep(0.5)


def do_sth(lock):
    logging.debug("work starting")
    num_tries = 0
    num_acquires = 0
    while num_acquires < 3:
        time.sleep(0.5)
        logging.debug("Trying lock acquire")
        have_it = lock.acquire(0)  # 从当前线程中得知锁是否被其他线程占用可以向 acquire() 传递 False 来立即得知。
        try:
            num_tries += 1
            if have_it:
                logging.debug("Iteration %d: Acquired", num_tries)
                num_acquires += 1
            else:
                logging.debug("Iteration %d: Not Acquired", num_tries)
        finally:
            if have_it:
                lock.release()
    logging.debug("Done after %d acquires", num_tries)


logging.info("")
logging.info("二、 锁的尝试获取")
lock = threading.Lock()
t1 = threading.Thread(target=lock_holder, name="lock_holder", args=(lock,), daemon=True)
t2 = threading.Thread(target=do_sth, name="worker", args=(lock,))
t1.start()
t2.start()
t2.join()
time.sleep(1)

logging.info("")
logging.info("三、 可重入锁和普通锁的简单对比")
# 获取普通锁不释放，检查是被占用的；获取可重入锁不释放，则一直都可用。
lock = threading.Lock()
logging.debug(f"first try, {lock.acquire()}")
logging.debug(f"second try, {lock.acquire(0)}")

rlock = threading.RLock()
logging.debug(f"first try, {rlock.acquire()}")
logging.debug(f"second try, {rlock.acquire(0)}")
logging.debug(f"third try, {rlock.acquire(0)}")


# 锁的上下文管理器，worker_with() 和 worker_no_with() 所实现的功能一模一样的。
def worker_with(lock):
    with lock:
        logging.debug("lock acquired via with")


def worker_no_with(lock):
    lock.acquire()
    try:
        logging.debug("lock acquired via try")
    finally:
        lock.release()


time.sleep(1)

logging.info("")
logging.info("四、 通过上下文管理器使用锁")
lock = threading.Lock()
w = threading.Thread(target=worker_with, args=(lock,))
nw = threading.Thread(target=worker_no_with, args=(lock,))

w.start()
nw.start()
