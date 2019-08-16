import random
import threading
import logging

logging.basicConfig(
    level=logging.DEBUG, format="[%(levelname)s] (%(threadName)-10s) %(message)s"
)
## thread local
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

# local() 类可以在每个线程中创建一个用于隐藏值的对象容器。 local_data.value 在当前的线程设置任何值前，对于当前线程来说它都什么都没有。
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
