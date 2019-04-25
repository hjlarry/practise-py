import multiprocessing
import time

# 共享全局变量通信不能用于多进程，可以适用于多线程
# Manager()提供了用于进程间共享通信的dict, list , Namespace, Queue, Event, Lock等


def worker(d, key, value):
    d[key] = value


print("dict example")
mgr = multiprocessing.Manager()
d = mgr.dict()
jobs = [multiprocessing.Process(target=worker, args=(d, i, i * 2)) for i in range(10)]
for j in jobs:
    j.start()
for j in jobs:
    j.join()
print(d.items())
print()

## Shared Namespaces
def producer(ns, event):
    ns.value = "This is the value"
    event.set()


def consumer(ns, event):
    try:
        print("Before event: {}".format(ns.value))
    except Exception as err:
        print("Before event, error:", str(err))
    event.wait()
    print("After event:", ns.value)


print("namespace example")
mgr = multiprocessing.Manager()
namespace = mgr.Namespace()
event = multiprocessing.Event()
p = multiprocessing.Process(target=producer, args=(namespace, event))
c = multiprocessing.Process(target=consumer, args=(namespace, event))

c.start()
p.start()

c.join()
p.join()
print()
time.sleep(1)

print("修改可变对象的值，但namespace并不会跟着自动去更新")


def producer1(ns, event):
    # DOES NOT UPDATE GLOBAL VALUE!
    ns.my_list.append("This is the value")
    event.set()


def consumer1(ns, event):
    print("Before event:", ns.my_list)
    event.wait()
    print("After event :", ns.my_list)


mgr = multiprocessing.Manager()
namespace = mgr.Namespace()
namespace.my_list = []

event = multiprocessing.Event()
p = multiprocessing.Process(target=producer1, args=(namespace, event))
c = multiprocessing.Process(target=consumer1, args=(namespace, event))

c.start()
p.start()

c.join()
p.join()
