import queue
import functools
import threading

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
