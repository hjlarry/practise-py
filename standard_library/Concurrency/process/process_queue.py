import multiprocessing
import time
import queue

# 标准库的queue.Queue只是线程安全的，无法用于多进程编程
def producer(q):
    q.put("a")
    time.sleep(2)


def consumer(q):
    time.sleep(1)
    print(q.get())


# print("test queue.Queue()")  运行结果会阻塞，无法继续
# q = queue.Queue(10)
# my_pro = multiprocessing.Process(target=producer, args=(q,))
# my_con = multiprocessing.Process(target=consumer, args=(q,))
# my_pro.start()
# my_con.start()
# my_pro.join()
# my_con.join()
# time.sleep(1)
print("test multiprocessing.Queue()")
q = multiprocessing.Queue(10)
my_pro = multiprocessing.Process(target=producer, args=(q,))
my_con = multiprocessing.Process(target=consumer, args=(q,))
my_pro.start()
my_con.start()
my_pro.join()
my_con.join()
time.sleep(1)
print()

print("test queue save own obj")


class MyFancyClass:
    def __init__(self, name):
        self.name = name

    def do_sth(self):
        proc_name = multiprocessing.current_process().name
        print(f"Doing sth for {self.name} in {proc_name}")


def worker(q):
    obj = q.get()
    obj.do_sth()


queue = multiprocessing.Queue()
p1 = multiprocessing.Process(target=worker, args=(queue,))
p2 = multiprocessing.Process(target=worker, args=(queue,))
p1.start()
p2.start()
queue.put(MyFancyClass("sdjaklsdj"))
queue.put(MyFancyClass("gahahah"))
# wait for worker to finish
queue.close()
queue.join_thread()
p1.join()
p2.join()
print()

# manage several workers consuming data from a JoinableQueue and passing results back to the parent process
class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print(f"{proc_name} Exiting")
                self.task_queue.task_done()
                break
            print(f"{proc_name}:{next_task}")
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)


class Task:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(0.1)  # pretend to take time to do the work
        return f"{self.a} * {self.b} = {self.a*self.b}"

    def __str__(self):
        return f"{self.a} * {self.b}"


# JoinableQueue比Queue多了task_done()和join()方法，前者用于通知生产者任务处理完成，而join()可以用来阻塞直到队列中所有item都调用task_done()为止
tasks = multiprocessing.JoinableQueue()
results = multiprocessing.Queue()

# Start consumers
num_consumers = multiprocessing.cpu_count() * 2
print(f"create {num_consumers} consumers")

consumers = [Consumer(tasks, results) for _ in range(num_consumers)]
for w in consumers:
    w.start()

num_jobs = 10
for i in range(num_jobs):
    tasks.put(Task(i, i))

# add a posion pill for each consumer
for i in range(num_consumers):
    tasks.put(None)

# wait for all task to finish
tasks.join()
while num_jobs:
    result = results.get()
    print("Result:", result)
    num_jobs -= 1

