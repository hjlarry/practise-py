# 使用线程允许一个程序在同一个进程空间中并发运行多个操作。
# 线程运行的两种方式分别为方法、继承 Thread 类
import threading
import time

def worker(num):
    """thread worker function"""
    print(f'Worker {num}')
    print(threading.current_thread().getName())

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()


class MyThread(threading.Thread):
    def run(self):   # 重写run方法，没有运行target
        logging.debug('this running')
        logging.debug(self._args)
for i in range(5):
    t = MyThread(target=worker, args=('dss','asa'))
    t.start()


# Timer 提供了一个继承 Thread 的例子，也包含在 threading 模块中。Timer 在延迟一段时间后启动工作，他可以在延迟的这段时间内任何时间点取消。
def delayed():
    logging.debug('worker running')
    
t1 = threading.Timer(0.3, delayed)
t2 = threading.Timer(0.3, delayed)
t1.setName('t1')
t2.setName('t2')
logging.debug('starting timers')
t1.start()
t2.start()

logging.debug('waiting before canceling %s', t2.getName())
time.sleep(0.2)
logging.debug('canceling %s', t2.getName())
t2.cancel()  # 在delay参数内可以取消执行
logging.debug('done')

#%% [markdown]
# ## 线程同步

#%%
def wait_for_event(e):
    logging.debug('wait_for_event starting')
    event_is_set = e.wait()  
    logging.debug('event set: %s', event_is_set)
    
def wait_for_event_timeout(e, t):
    while not e.is_set():
        logging.debug('wait_for_event_timeout starting')
        event_is_set = e.wait(t)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other work')


#%%
e = threading.Event()
t1 = threading.Thread(name='block', target=wait_for_event, args=(e,))
t2 = threading.Thread(name='nonblock', target=wait_for_event_timeout, args=(e,2))
t1.start()
t2.start()
logging.debug('Waiting before calling event.set()')
time.sleep(0.3)
e.set()
logging.debug('Event is set')

#%% [markdown]
# wait() 方法可以接收一个参数，表示事件等待的超时时间

#%%
import random
class Counter:
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start
    def increment(self):
        logging.debug('Waiting for lock')
        self.lock.acquire()
        try:
            logging.debug('Lock acquired')
            self.value = self.value + 1    # 获取锁后对值操作，保证多个线程同时修改其内部状态不会出问题
        finally:
            self.lock.release()
            
def worker(c):
    for i in range(2):
        pause = random.random()
        logging.debug('Sleeping %0.02f', pause)
        time.sleep(pause)
        c.increment()
    logging.debug('Done')
    
counter = Counter()
for i in range(2):
    t = threading.Thread(target=worker, args=(counter, ), name=str(i))
    t.start()
    
logging.debug('Waiting for work threads')
for t in threading.enumerate():
    if t.getName() == str(0) or t.getName() == str(1):
        t.join()
logging.debug('Count value %d', counter.value)


#%%
def lock_holder(lock):
    logging.debug('Starting')
    while True:
        lock.acquire()
        try:
            logging.debug('Holding')
            time.sleep(1)
        finally:
            logging.debug('Not holding')
            lock.release()
        time.sleep(0.5)

def worker(lock):
    logging.debug('work starting')
    num_tries = 0
    num_acquires = 0
    while num_acquires < 3:
        time.sleep(0.5)
        logging.debug('Trying lock acquire')
        have_it = lock.acquire(0) # 从当前线程中得知锁是否被其他线程占用可以向 acquire() 传递 False 来立即得知。
        try:
            num_tries += 1
            if have_it:
                logging.debug('Iteration %d: Acquired', num_tries)
                num_acquires += 1
            else:
                logging.debug('Iteration %d: Not Acquired', num_tries)
        finally:
            if have_it:
                lock.release()
    logging.debug('Done after %d acquires', num_tries)
    
lock = threading.Lock()
t1 = threading.Thread(target=lock_holder, name='lock_holder', args=(lock,), daemon=True)
t2 = threading.Thread(target=worker, name='worker', args=(lock,))          
t1.start()
t2.start()

#%% [markdown]
# 为了获取三次锁而尝试了8次。

#%%
import threading
lock = threading.Lock()
print('first try,', lock.acquire())
print('second try,', lock.acquire(0))

rlock = threading.RLock()
print('first try,', rlock.acquire())
print('second try,', rlock.acquire(0))
print('third try,', rlock.acquire(0))
# acquire() 两次，release() 也要两次


#%%
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)
# worker_with() 和 worker_no_with() 所实现的功能一模一样的。
def worker_with(lock):
    with lock:
        logging.debug('lock acquired via with')
def worker_no_with(lock):
    lock.acquire()
    try:
        logging.debug('lock acquired via try')
    finally:
        lock.release()
lock = threading.Lock()
w = threading.Thread(target=worker_with, args=(lock,))
nw = threading.Thread(target=worker_no_with, args=(lock,))

w.start()
nw.start()


#%%
import time
def consumer(cond):
    logging.debug('Starting consumer')
    with cond:
        cond.wait()
        logging.debug('Resource is available to consumer')
def producer(cond):
    logging.debug('Starting producer')
    with cond:
        
        cond.notifyAll()
        logging.debug('making resource available1')
        
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-2s) %(message)s',
)
condition = threading.Condition()
c1 = threading.Thread(target=consumer, args=(condition, ), name='c1')
c2 = threading.Thread(target=consumer, args=(condition, ), name='c2')
p = threading.Thread(target=producer, args=(condition, ), name='p')
c1.start()
time.sleep(2)
c2.start()
time.sleep(2)
p.start()

#%% [markdown]
# 除了使用 Events，另一种同步线程的方法是使用 Condition 对象。 Condition 使用了 Lock，所以它会绑定共享的资源，也就会让多个线程等待资源更新完成。
# 
# 屏障」（Barrier）是另一种线程同步的机制。每个 Barrier 会建立起一个控制点，所有处在其中的线程都会被阻塞，直到所有的线程都到达这个控制点。它会让所有的线程单独启动，然后在它们全都准备好执行下一步前先阻塞住。

#%%
def worker(barrier):
    print(threading.current_thread().name, f"wait for barrier with {barrier.n_waiting} others")
    worker_id = barrier.wait()
    print(f"{threading.current_thread().name} after barrier  {worker_id}")

NUM_T = 3
barrier = threading.Barrier(NUM_T)
threads = [threading.Thread(name=f'worker-{i}', target=worker, args=(barrier,)) for i in range(NUM_T)]
for t in threads:
    print(t.name, 'starting')
    t.start()
    time.sleep(0.1)

for t in threads:
    t.join()


#%%
def worker(barrier):
    print(threading.current_thread().name, f"wait for barrier with {barrier.n_waiting} others")
    try:
        worker_id = barrier.wait()
    except threading.BrokenBarrierError:
        print(f'{threading.current_thread().name} aborting')
    else:
        print(f"{threading.current_thread().name} after barrier  {worker_id}")

NUM_T = 3
barrier = threading.Barrier(NUM_T + 1)
threads = [threading.Thread(name=f'worker-{i}', target=worker, args=(barrier,)) for i in range(NUM_T)]
for t in threads:
    print(t.name, 'starting')
    t.start()
    time.sleep(0.1)
barrier.abort()
for t in threads:
    t.join()

#%% [markdown]
# Barrier 的 abort() 方法会导致所有等待中的线程接收到一个 BrokenBarrierError。 我们可以使用此方法来告知那些被阻塞住的线程该结束了。这次我们将 Barrier 设置成比实际开始的线程多一个，这样所有的线程就会被阻塞住，我们调用 abort() 就可以引起 BrokenBarrierError 了。

#%%
class ActivePool:
    def __init__(self):
        self.active = []
        self.lock = threading.Lock()
    def make_active(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug(f"Running {self.active}")
    def make_inactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug(f"Running {self.active}")
            
def worker(s, pool):
    logging.debug('Wait for join the pool')
    with s:
        name = threading.current_thread().getName()
        pool.make_active(name)
        time.sleep(1)
        pool.make_inactive(name)
        
pool = ActivePool()
s = threading.Semaphore(2)

for i in range(4):
    t = threading.Thread(target=worker, name=str(i), args=(s, pool))
    t.start()
        

#%% [markdown]
# 有时我们需要允许多个工作函数在同一时间访问同一个资源，但我们也要限制可访问的总数。  
# ActivePool 类只是用来追踪给定时刻下哪些线程在工作的。如果是实际情况中，资源池一般还要分配连接或者其他值给新的活动线程，并且当线程结束后回收这些值。
# 
# ## thread local

#%%
import random
def show_value(data):
    try:
        val=data.value
    except AttributeError:
        logging.debug('Not value yet')
    else:
        logging.debug('value=%s', val)
        
def worker(data):
    show_value(data)
    data.value = random.randint(1,100)
    show_value(data)
    
local_data = threading.local()
show_value(local_data)
local_data.value = 1000
show_value(local_data)

for i in range(2):
    t = threading.Thread(target=worker, args=(local_data,))
    t.start()

#%% [markdown]
# local() 类可以在每个线程中创建一个用于隐藏值的对象容器。 local_data.value 在当前的线程设置任何值前，对于当前线程来说它都什么都没有。

#%%
class MyLocal(threading.local):
    def __init__(self, value):
        super().__init__()
        logging.debug('Initializing %r', self)
        self.value = value
        
    
local_data = MyLocal(1000)
show_value(local_data)

for i in range(2):
    t = threading.Thread(target=worker, args=(local_data,))
    t.start()


