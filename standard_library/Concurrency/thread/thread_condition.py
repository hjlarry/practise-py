"""
Condition实际上是两级锁，创建Condition对象时会存储一个可重入锁在self._lock。
with进入的时候，实际上调用了self._lock.acquire()。
后续使用时调用wait(), 会新拿一个锁放在self._waiters双端队列中。
notify()时会从self._waiters中拿出锁去释放。

基于Condition实现的有:Semaphore, Barrier, Event, queue.Queue
"""


import time
import threading
import logging


def consumer(cond):
    logging.debug("Starting consumer")
    with cond:
        cond.wait()
        logging.debug("Resource is available to consumer")


def producer(cond):
    logging.debug("Starting producer")
    with cond:
        cond.notifyAll()
        logging.debug("making resource available1")


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s (%(threadName)-2s) %(message)s"
)
condition = threading.Condition()
c1 = threading.Thread(target=consumer, args=(condition,), name="c1")
c2 = threading.Thread(target=consumer, args=(condition,), name="c2")
p = threading.Thread(target=producer, args=(condition,), name="p")
c1.start()
time.sleep(1)
c2.start()
time.sleep(1)
p.start()


class XiaoAiLock(threading.Thread):
    def __init__(self, lock):
        super().__init__()
        self.lock = lock
        self.name = "小爱同学"

    def run(self):
        self.lock.acquire()
        print(f"{self.name}: hello")
        self.lock.release()

        self.lock.acquire()
        print(f"{self.name}: 我们来对诗吧")
        self.lock.release()

        self.lock.acquire()
        print(f"{self.name}: 床前明月光")
        self.lock.release()


class TianMaoLock(threading.Thread):
    def __init__(self, lock):
        super().__init__()
        self.lock = lock
        self.name = "天猫精灵"

    def run(self):
        self.lock.acquire()
        print(f"{self.name}: Hi")
        self.lock.release()

        self.lock.acquire()
        print(f"{self.name}: 好的")
        self.lock.release()

        self.lock.acquire()
        print(f"{self.name}: 疑是地上霜")
        self.lock.release()


lock = threading.RLock()
xiaoai = XiaoAiLock(lock)
tianmao = TianMaoLock(lock)
xiaoai.start()
tianmao.start()

print("Condition Example:")


class XiaoAiCond(threading.Thread):
    def __init__(self, cond):
        super().__init__()
        self.cond = cond
        self.name = "小爱同学"

    def run(self):
        with self.cond:

            print(f"{self.name}: hello")
            self.cond.notify()
            self.cond.wait()

            print(f"{self.name}: 我们来对诗吧")
            self.cond.notify()
            self.cond.wait()

            print(f"{self.name}: 床前明月光")
            self.cond.notify()
            self.cond.wait()


class TianMaoCond(threading.Thread):
    def __init__(self, cond):
        super().__init__()
        self.cond = cond
        self.name = "天猫精灵"

    def run(self):
        with self.cond:
            self.cond.wait()
            print(f"{self.name}: Hi")
            self.cond.notify()

            self.cond.wait()
            print(f"{self.name}: 好的")
            self.cond.notify()

            self.cond.wait()
            print(f"{self.name}: 疑是地上霜")
            self.cond.notify()


cond = threading.Condition()
xiaoai = XiaoAiCond(cond)
tianmao = TianMaoCond(cond)

# 需要注意启动的顺序
tianmao.start()
xiaoai.start()
