import time
import threading

print("一、 有否使用Semaphore的对比")


def get_detail_url():
    for i in range(20):
        t = threading.Thread(target=get_detail_content, args=(i,))
        t.start()


def get_detail_content(i):
    time.sleep(1)
    print("get detail page content", i)


t = threading.Thread(target=get_detail_url)
t.start()
t.join()


def get_url_sem(sem):
    for i in range(20):
        sem.acquire()
        t = threading.Thread(target=get_content_sem, args=(i, sem))
        t.start()


def get_content_sem(i, sem):
    time.sleep(1)
    print("use semaphore get detail page content", i)
    sem.release()


# Semaphore通过锁控制了并发任务的数量，内部实现是基于Condition的，初始化传入了self._value，每次acquire则_value-1，_value为0时调用Condition的wait()
sem = threading.Semaphore(3)
t_sem = threading.Thread(target=get_url_sem, args=(sem,))
t_sem.start()
t_sem.join()

time.sleep(1)
print()
print("二、 资源池示例")
# 有时我们需要允许多个工作函数在同一时间访问同一个资源，但我们也要限制可访问的总数。
# ActivePool 类只是用来追踪给定时刻下哪些线程在工作的。如果是实际情况中，资源池一般还要分配连接或者其他值给新的活动线程，并且当线程结束后回收这些值。
class ActivePool:
    def __init__(self):
        self.active = []
        self.lock = threading.Lock()

    def make_active(self, name):
        with self.lock:
            self.active.append(name)
            print(f"Running {self.active}")

    def make_inactive(self, name):
        with self.lock:
            self.active.remove(name)
            print(f"Running {self.active}")


def worker(s, pool):
    print("Wait for join the pool")
    with s:
        name = threading.current_thread().getName()
        pool.make_active(name)
        time.sleep(1)
        pool.make_inactive(name)


pool = ActivePool()
s = threading.Semaphore(2)

for i in range(8):
    t = threading.Thread(target=worker, name=str(i), args=(s, pool))
    t.start()
