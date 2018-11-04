#%%
import sched
import time

scheduler = sched.scheduler(time.time, time.sleep)


def print_event(name, start):
    now = time.time()
    elapsed = int(now - start)
    print(f"Event:{time.ctime(now)} ,elapsed={elapsed}, name={name}")


start = time.time()
print("Start:", time.ctime(start))
# 参数为代表延迟的数字、优先级、被调用函数，函数参数元组
scheduler.enter(2, 1, print_event, ("first", start))
scheduler.enter(3, 1, print_event, ("second", start))
scheduler.run()

#%%
def long_event(name):
    print("begin event:", time.ctime(time.time()), name)
    time.sleep(2)
    print("after event:", time.ctime(time.time()), name)


print("Start:", time.ctime(start))
scheduler.enter(2, 1, long_event, ("first",))
# 阻塞事件会推迟下一事件的按计划执行
scheduler.enter(3, 1, long_event, ("second",))
scheduler.run()

#%%
def print_event1(name):
    print(f"print_Event1:{time.ctime(time.time())} ,name={name}")


now = time.time()
print("Start:", time.ctime(now))
# 同一计划时间的任务，使用enterabs(), 优先级数字小的先执行, enterabs()第一个参数是运行事件的时间
scheduler.enterabs(now + 2, 2, print_event1, ("first",))
scheduler.enterabs(now + 2, 1, print_event1, ("second",))
scheduler.run()

import threading

counter = 0


def incre_count(name):
    global counter
    print("EVENT:", time.ctime(time.time()), name)
    counter += 1
    print("now:", counter)


print("Start:", time.ctime(time.time()))
e1 = scheduler.enter(2, 1, incre_count, ("E1",))
e2 = scheduler.enter(3, 1, incre_count, ("E2",))

t = threading.Thread(target=scheduler.run)
t.start()

scheduler.cancel(e1)

t.join()
print('Final:', counter)
