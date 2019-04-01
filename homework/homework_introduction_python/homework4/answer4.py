# Server Side
from multiprocessing.managers import BaseManager
import queue
import random

host = "127.0.0.1"
port = 9030
authkey = b"secret"

tasks_queue = queue.PriorityQueue()


class RemoteManager(BaseManager):
    pass


def double(n):
    return n * 2


RemoteManager.register("get_queue", callable=lambda: tasks_queue)
mgr = RemoteManager(address=(host, port), authkey=authkey)
mgr.start()
tasks_queue = mgr.get_queue()
count = 0
while 1:
    if count < 5:
        pri = random.randint(1, 100)
        print(f"put :{pri}")
        tasks_queue.put((pri, double, pri))
        count += 1

# Client Side
from multiprocessing.managers import BaseManager

host = "127.0.0.1"
port = 9030
authkey = b"secret"


class RemoteManager(BaseManager):
    pass


def double(n):
    return n * 2


RemoteManager.register("get_queue")
mgr = RemoteManager(address=(host, port), authkey=authkey)
mgr.connect()

tasks_queue = mgr.get_queue()
count = 0
while 1:
    if tasks_queue.empty():
        break
    pri, task, arg = tasks_queue.get()
    print(f"[PRI:{pri}] {arg} * 2 = {task(arg)}")
    tasks_queue.task_done()
    time.sleep(0.1)
