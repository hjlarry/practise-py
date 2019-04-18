import threading
import time
import logging
from random import randint

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s (%(threadName)-2s) %(message)s"
)


def wait_for_event(e):
    logging.debug("wait_for_event starting")
    event_is_set = e.wait()
    logging.debug("event set: %s", event_is_set)


def wait_for_event_timeout(e, t):
    while not e.is_set():
        logging.debug("wait_for_event_timeout starting")
        # wait() 方法可以接收一个参数，表示事件等待的超时时间
        event_is_set = e.wait(t)
        logging.debug("event set: %s", event_is_set)
        if event_is_set:
            logging.debug("processing event")
        else:
            logging.debug("doing other work")


logging.info("一、 基础使用示例")
e = threading.Event()
t1 = threading.Thread(name="block", target=wait_for_event, args=(e,))
t2 = threading.Thread(name="nonblock", target=wait_for_event_timeout, args=(e, 2))
t1.start()
t2.start()
logging.debug("Waiting before calling event.set()")
time.sleep(0.3)
e.set()
logging.debug("Event is set")
time.sleep(1)

logging.info("")
logging.info("二、 生产消费者示例")
TIMEOUT = 2


def consumer(event, l):
    t = threading.currentThread()
    while 1:
        event_is_set = event.wait(TIMEOUT)
        if event_is_set:
            try:
                integer = l.pop()
                logging.debug(f"{integer} popped from list by {t.name}")
                event.clear()  # 重置事件状态
            except IndexError:
                # 因为有多个消费者，而每次只生产了一个数据，在列表里pop就会IndexError
                pass


def producer(event, l):
    t = threading.currentThread()
    while 1:
        integer = randint(10, 100)
        l.append(integer)
        logging.debug(f"{integer} appended to list by {t.name}")
        event.set()  # 设置事件
        time.sleep(1)


event = threading.Event()
l = []

threads = []
# 这个示例consumer2往往过很久才会轮到它执行，这可能取决于底层对于线程的选择？
for name in ("consumer1", "consumer2"):
    t = threading.Thread(name=name, target=consumer, args=(event, l))
    t.start()
    threads.append(t)

p = threading.Thread(name="producer1", target=producer, args=(event, l))
p.start()
threads.append(p)

for t in threads:
    t.join()
