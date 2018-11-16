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


logging.basicConfig(
    level=logging.DEBUG, format="[%(levelname)s] (%(threadName)-10s) %(message)s"
)
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
