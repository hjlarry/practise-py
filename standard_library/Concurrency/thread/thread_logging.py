import logging
import time
import threading

# logging 模块支持在日志信息中写入线程的名字，你可以用格式化代码 %(threadName)s 来得到它。
def worker():
    logging.debug("Starting")
    time.sleep(0.2)
    logging.debug("Exit")


def service():
    logging.debug("Starting")
    time.sleep(0.5)
    logging.debug("Exit")


t1 = threading.Thread(target=worker)
t2 = threading.Thread(target=service)
logging.basicConfig(
    level=logging.DEBUG, format="[%(levelname)s] (%(threadName)-10s) %(message)s"
)

t1.start()
t2.start()
