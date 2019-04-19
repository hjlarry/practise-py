import queue
import functools
import threading
import random
import time

print("一、先进先出型和后进先出队列")
# 先进先出型
q1 = queue.Queue()
for i in range(5):
    q1.put(i)

while not q1.empty():
    print(q1.get(), end=" ")
print()

# 后进先出型
q2 = queue.LifoQueue()
for i in range(5):
    q2.put(i)

while not q2.empty():
    print(q2.get(), end=" ")
print()
print()

print("二、优先级队列")
# 优先级队列
@functools.total_ordering
class Job:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print("New job", description)

    def __eq__(self, other):
        try:
            return self.priority == other.priority
        except AttributeError:
            raise NotImplementedError

    def __lt__(self, other):
        try:
            return self.priority < other.priority
        except AttributeError:
            raise NotImplementedError


q = queue.PriorityQueue()
q.put(Job(3, "mid level"))
q.put(Job(10, "low level"))
q.put(Job(1, "high level"))


def process_job(q):
    while True:
        next_job = q.get()
        print("Processing job", next_job.description)
        q.task_done()


workers = [
    threading.Thread(target=process_job, args=(q,)),
    threading.Thread(target=process_job, args=(q,)),
]

for w in workers:
    w.setDaemon(True)
    w.start()
q.join()

print()
print("三、生产消费者模型")


class Producer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            print(f"Producer notify: item N° {item} appended to queue by {self.name}")
            time.sleep(1)


class Consumer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            item = self.queue.get()
            print(f"Consumer notify : {item} popped from queue by {self.name}")
            self.queue.task_done()


q = queue.Queue()
t1 = Producer(q)
t2 = Consumer(q)
t3 = Consumer(q)
t4 = Consumer(q)
t1.start()
t2.start()
t3.start()
t4.start()
t1.join()
t2.join()
t3.join()
t4.join()
