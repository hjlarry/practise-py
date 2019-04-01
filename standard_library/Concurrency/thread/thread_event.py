import threading
import time
import logging


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


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s (%(threadName)-2s) %(message)s"
)
e = threading.Event()
t1 = threading.Thread(name="block", target=wait_for_event, args=(e,))
t2 = threading.Thread(name="nonblock", target=wait_for_event_timeout, args=(e, 2))
t1.start()
t2.start()
logging.debug("Waiting before calling event.set()")
time.sleep(0.3)
e.set()
logging.debug("Event is set")
