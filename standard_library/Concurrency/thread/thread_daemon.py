import logging
import time
import threading

# 设置为守护线程，则主线程结束时会kill掉守护线程
# t1.join()则会使守护线程持续执行下去，join参数timeout设置后，若超时线程并未结束，则join会返回，不会继续等待。
def daemon():
    logging.debug("Daemon Starting")
    time.sleep(0.2)
    logging.debug("Daemon Exit")


def non_daemon():
    logging.debug("Starting")
    logging.debug("Exit")


t1 = threading.Thread(target=daemon, daemon=True, name="daemon")
t2 = threading.Thread(target=non_daemon, name="non-daemon")
logging.basicConfig(
    level=logging.DEBUG, format="[%(levelname)s] (%(threadName)-10s) %(message)s"
)

t1.start()
t2.start()
