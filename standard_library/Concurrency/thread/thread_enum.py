import random
import logging
import time
import threading

# 枚举所有线程
def worker():
    pause = random.randint(1, 5) / 10
    logging.debug("Daemon Starting sleep %0.2f", pause)
    time.sleep(pause)
    logging.debug("Daemon Exit")


logging.basicConfig(
    level=logging.DEBUG, format="[%(levelname)s] (%(threadName)-10s) %(message)s"
)
for i in range(3):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

main_thread = threading.main_thread()

print(threading.enumerate())
for t in threading.enumerate():
    if t is main_thread:
        continue
    logging.debug("%s joining", t.getName())
    t.join()
