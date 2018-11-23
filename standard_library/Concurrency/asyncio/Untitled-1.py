#%% [markdown]
# ## 

#%%

#%% [markdown]
# ## 

#%%
import asyncio


#%% [markdown]
# ## 

#%%

#%% [markdown]
# ## 

#%%
import asyncio


#%% [markdown]
# ## Scheduling a Callback with a Delay

#%%
import asyncio


#%% [markdown]
# ## Scheduling a Callback for a Specific Time

#%%
import asyncio
import time

#%% [markdown]
# ## Waiting for a Future

#%%
import asyncio

def mark_done(future, result):
    print(f"setting future result for {result!r}")
    future.set_result(result)
    
event_loop = asyncio.get_event_loop()
try:
    all_done = asyncio.Future()
    print('scheduling mark_done')
    event_loop.call_soon(mark_done, all_done, 'the result111')
    result = event_loop.run_until_complete(all_done)
    print('return result',result)
finally:
    event_loop.close()
print('final result ',all_done.result())


#%%
# future with await
import asyncio

def mark_done(future, result):
    print(f"setting future result for {result!r}")
    future.set_result(result)
    
async def main(loop):
    all_done = asyncio.Future()
    print('scheduling mark_done')
    loop.call_soon(mark_done, all_done, 'the result222')
    result =  await all_done
    print('return result',result)
    
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

#%% [markdown]
# ## Future Callbacks

#%%
import asyncio
import functools

def callback(future, n):
    print(f"{n}: future done: {future.result()}")
    
async def reg_callbacks(all_done):
    all_done.add_done_callback(functools.partial(callback, n=1))
    all_done.add_done_callback(functools.partial(callback, n=3))
    
async def main(all_done):
    await reg_callbacks(all_done)
    all_done.set_result('sdasdsa')
    
event_loop = asyncio.get_event_loop()
try:
    all_done = asyncio.Future()
    event_loop.run_until_complete(main(all_done))
finally:
    event_loop.close()

#%% [markdown]
# ## Starting a Task

#%%
import asyncio
    
async def task_func():
    print('exe task')
    return 'task_result'
    
async def main(loop):
    print('create task')
    task = loop.create_task(task_func())
    return_value = await task
    print(return_value)
    
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

#%% [markdown]
# ## Canceling a Task

#%%
import asyncio
    
async def task_func():
    print('exe task')
    return 'task_result'
    
async def main(loop):
    print('create task')
    task = loop.create_task(task_func())
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print('canceled task')
    else:
        print(task.result())
    
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()


#%%
import asyncio
    
async def task_func():
    print('in task func, sleeping')
    try:
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        print('task_func cancelled',3)
        raise
    return 'task_result'

def task_cancel(t):
    print('in task_cancel')
    t.cancel()
    print('task_cancel',2)
    
async def main(loop):
    print('create task')
    task = loop.create_task(task_func())
    loop.call_soon(task_cancel, task)
    try:
        await task
    except asyncio.CancelledError:
        print('main also cancel',4)
    else:
        print(task.result())
    
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

#%% [markdown]
# ## Creating Tasks from Coroutines

#%%
import asyncio

async def wrapped():
    print(5)
    return 'result-wrapped'

async def inner(task):
    print(4)
    print('inner', task)
    result = await task
    print('task return ', result)
    
async def starter():
    print(2)
    task = asyncio.ensure_future(wrapped())
    print(3)
    await inner(task)
    print(6)
    

event_loop = asyncio.get_event_loop()
try:
    print(1)
    event_loop.run_until_complete(starter())
finally:
    event_loop.close()

#%% [markdown]
# ## Waiting for Multiple Coroutines

#%%
import asyncio

async def phase(i):
    print('in phase', i)
    await asyncio.sleep(0.1*i)
    print('done with phase', i)
    return f"phase result {i}"

async def main(num):
    print('main start')
    phases = [phase(i) for i in range(num)]
    print('wait phases complete')
    completed, pending = await asyncio.wait(phases)
    results = [t.result() for t in completed]
    print(results,1)
    
event_loop = asyncio.get_event_loop()
try:
    print(1)
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()


#%%
# wait timeout
import asyncio

async def phase(i):
    print('in phase', i)
    try:
        await asyncio.sleep(0.1*i)
    except asyncio.CancelledError:
        print('phase cancel', i)
        raise
    else:
        print('done with phase', i)
        return f"phase result {i}"

async def main(num):
    print('main start')
    phases = [phase(i) for i in range(num)]
    print('wait phases complete')
    completed, pending = await asyncio.wait(phases, timeout=0.1)
    print(f'{len(completed)} completed, {len(pending)} pending')
    if pending:
        print('to cancel tasks')
        for t in pending:
            t.cancel()
    print('exiting main')
    
event_loop = asyncio.get_event_loop()
try:
    print(1)
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()

#%% [markdown]
# ## Gathering Results from Coroutines

#%%
import asyncio

async def phase1():
    print('in phase1')
    await asyncio.sleep(3)
    print('done with phase1')
    return f"phase result 1"

async def phase2():
    print('in phase2')
    await asyncio.sleep(1)
    print('done with phase2')
    return f"phase result 2"

async def main():
    result = await asyncio.gather(phase1(), phase2())
    print(result)
    
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main())
finally:
    event_loop.close()

#%% [markdown]
# ## Handling Background Operations as They Finish

#%%
import asyncio

async def phase(i):
    print('in phase', i)
    await asyncio.sleep((1-0.1*i))
    print('done with phase', i)
    return f"phase result {i}"

async def main(num):
    print('main start')
    phases = [phase(i) for i in range(num)]
    print('wait phases complete')
    results = []
    for next_to_complete in asyncio.as_completed(phases):
        answer = await next_to_complete
        print("received ", answer)
        results.append(answer)
    print(results,1)
    return results
    
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()

#%% [markdown]
# ## Locks

#%%
import asyncio
import functools

def unlock(lock):
    print("callback release the lock")
    lock.release()
    
async def coro1(lock):
    print('coro1 wait the lock')
    with await lock:
        print('coro1 acquire lock')
    print('coro1 release lock')
    
async def coro2(lock):
    print('coro2 wait the lock')
    await lock
    try:
        print('coro2 acquire lock')
    finally:
        print('coro2 release lock')
        lock.release()
        
async def main(loop):
    lock = asyncio.Lock()
    await lock.acquire()
    print('lock acquired', lock.locked())
    
    # schedule a callback to unlock the lock
    loop.call_later(2, functools.partial(unlock, lock))
    
    await asyncio.wait([coro1(lock), coro2(lock)])
    
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

#%% [markdown]
# ## Events

#%%
import asyncio
import functools

def set_event(event):
    print("set event in callback ")
    event.set()
    
async def coro1(event):
    print('coro1 wait the event')
    await event.wait()
    print('coro1 triggled')
    
async def coro2(event):
    print('coro2 wait the event')
    await event.wait()
    print('coro2 triggled')
        
async def main(loop):
    event = asyncio.Event()
    print('event state a', event.is_set())
    
    loop.call_later(2, functools.partial(set_event, event))
    
    await asyncio.wait([coro1(event), coro2(event)])
    print('event state b', event.is_set())
    
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

#%% [markdown]
# ## Conditions

#%%
import asyncio

async def consumer(condition, n):
    with await condition:
        print(f'consumer {n} is waiting')
        await condition.wait()
        print(f'consumer {n} trigger')
    print(f'consumer {n} end')
    
async def manipulate_condition(condition):
    print('Starting manipulate')
    
    # wait for consumer start
    await asyncio.sleep(0.1)
    
    for i in range(1,3):
        with await condition:
            print(f'notifying {i} consumers')
            condition.notify(n=i)
        await asyncio.sleep(2)
    with await condition:
        print('notifying remain consumers')
        condition.notify_all()
        
async def main(loop):
    condition = asyncio.Condition()
    consumers = [consumer(condition, i) for i in range(5)]
    loop.create_task(manipulate_condition(condition))
    await asyncio.wait(consumers)
    
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

#%% [markdown]
# ## Queues

#%%
import asyncio

async def consumer(n, q):
    print(f"consumer {n} starting")
    while True:
        print(f"consumer {n} wait for item")
        item = await q.get()
        print(f"consumer {n} get {item}")
        if item is None:
            # None is the signal to stop.
            q.task_done()
            break
        else:
            await asyncio.sleep(0.01*item)
            q.task_done()
    print(f"consumer {n} end")
    
async def producer(q, num_workers):
    print("producer starting")
    # Add some numbers to the queue to simulate jobs
    for i in range(num_workers *3):
        await q.put(i)
        print(f"producer add task {i} to queue")
    
    print("producer add stop signal to queue")
    for i in range(num_workers):
        await q.put(None)
    print("producer wait for queue to empty")  
    await q.join()
    print("producer ending")
    
async def main(loop, num_consumers):
    q = asyncio.Queue(maxsize=num_consumers)
    consumers = [loop.create_task(consumer(i, q)) for i in range(num_consumers)]
    prod = loop.create_task(producer(q, num_consumers))
    await asyncio.wait(consumers + [prod])
    
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop, 2))
finally:
    event_loop.close()

#%% [markdown]
# ## Interacting with Domain Name Services

#%%
import asyncio
import logging
import socket
import sys


TARGETS = [
    ('pymotw.com', 'https'),
    ('doughellmann.com', 'https'),
    ('python.org', 'https'),
]

async def main(loop, targets):
    for target in targets:
        info = await loop.getaddrinfo(*target, proto=socket.IPPROTO_TCP)
        print(info)


#%%
event = asyncio.get_event_loop()
try:
    event.run_until_complete(main(event, TARGETS))
finally:
    event.close()


#%%
import asyncio
TARGETS = [
    ('66.33.211.242', 443),
    ('104.130.43.121', 443),
]
async def main(loop, targets):
    for target in targets:
        info = await loop.getnameinfo(target)
        print(info)
event = asyncio.get_event_loop()
try:
    event.run_until_complete(main(event, TARGETS))
finally:
    event.close()

#%% [markdown]
# ## Working with Subprocesses
# ### Using the Protocol Abstraction with the Subprocesses

#%%
import asyncio
import functools

async def run_df(loop):
    print('in run_df')
    cmd_done = asyncio.Future(loop=loop)
    factory = functools.partial(DFProtocol, cmd_done)
    # use subprocess_exec() to launch the process and tie it to a protocol class
    # that know how to read the df command output and parse it
    proc = loop.subprocess_exec(factory, 'df','-hl', stdin=None, stderr=None)
    try:
        print('launching process')
        transport, protocol = await proc
        print('wait process to complete')
        await cmd_done
    finally:
        transport.close()
    return cmd_done.result()

# the method of the protocol class are called automaticalley based on I/O events for the subprocess. 
# Because both the stdin and stderr arguments are set to None, those communication channels are not connected to the new process.
class DFProtocol(asyncio.SubprocessProtocol):
    FD_NAMES = ['stdin', 'stdout', 'stderr']
    def __init__(self, done_futures):
        self.done = done_futures
        self.buffer = bytearray()
        super().__init__()
    def connection_made(self, transport):
        print('process started ', transport.get_pid())
        self.transport = transport
    def pipe_data_received(self, fd, data):
        print(f"read {len(data)} bytes from {self.FD_NAMES[fd]}")
        if fd == 1:
            self.buffer.extend(data)
    def process_exited(self):
        print('process exited')
        return_code = self.transport.get_returncode()
        print('return code ', return_code)
        if not return_code:
            cmd_output = bytes(self.buffer).decode()
            results = self._parse_results(cmd_output)
        else:
            results = []
        self.done.set_result((return_code, results))
    def _parse_results(self, output):
        print('paesing results')
        if not output:
            return []
        lines = output.splitlines()
        headers = lines[0].split()
        devices = lines[1:]
        results = [dict(zip(headers, line.split())) for line in devices]
        return results
event_loop = asyncio.get_event_loop()
try:
    return_code, results = event_loop.run_until_complete(run_df(event_loop))
finally:
    event_loop.close()
    
if return_code:
    print('error exit', return_code)
else:
    print('\n Free space:')
    # In shell can get the free space, but in jupyter can not
    for r in results:
        print('{Mounted:25}:{Avail}'.format(**r))
        
    

#%% [markdown]
# ### Calling Subprocesses with the Coroutines and Streams

#%%
import asyncio


def _parse_results(output):
        print('parseing results')
        if not output:
            return []
        lines = output.splitlines()
        headers = lines[0].split()
        devices = lines[1:]
        results = [dict(zip(headers, line.split())) for line in devices]
        return results
    
async def run_df():
    print('in run_df')
    buffer = bytearray()
    create = asyncio.create_subprocess_exec('df','-hl', stdout=asyncio.subprocess.PIPE)
    print('launching process')
    proc = await create
    print('process started at ', proc.pid)
    while True:
        line = await proc.stdout.readline()
        print(f"read {line!r}")
        if not line:
            print("no more output from command")
            break
        buffer.extend(line)
    print('waiting for process to complete')
    await proc.wait()
    return_code = proc.returncode
    print('return code ', return_code)
    if not return_code:
        cmd_output = bytes(buffer).decode()
        results = _parse_results(cmd_output)
    else:
        results = []
    return (return_code, results)

event_loop = asyncio.get_event_loop()
try:
    return_code, results = event_loop.run_until_complete(run_df())
finally:
    event_loop.close()
    
if return_code:
    print('error exit', return_code)
else:
    print('\n Free space:')
    for r in results:
        print('{Mounted:25}:{Avail}'.format(**r))
        
    

#%% [markdown]
# ### Sending Data to a Subprocess

#%%
import asyncio

async def to_upper(input):
    print('in to_upper')
    create = asyncio.create_subprocess_exec('tr', '[:lower:]', '[:upper:]', stdout=asyncio.subprocess.PIPE, stdin=asyncio.subprocess.PIPE)
    print('lanuching process')
    proc = await create
    print('pid ', proc.pid)
    print('communication with process')
    stdout, stderr = await proc.communicate(input.encode())
    print('waiting for process to complete')
    await proc.wait()
    return_code = proc.returncode
    print('return code ', return_code)
    if not return_code:
        results = bytes(stdout).decode()
    else:
        results = ''
    return (return_code, results)

MESSAGE = """
this message Will be converted to all caps
"""
event_loop = asyncio.get_event_loop()
try:
    return_code, results = event_loop.run_until_complete(to_upper(MESSAGE))
finally:
    event_loop.close()
    
if return_code:
    print('error exit', return_code)
else:
    print(f'Original: {MESSAGE!r}')
    print(f'Changed: {results!r}')

#%% [markdown]
# ## Receiving Unix Signals

#%%
import asyncio
import functools
import os
import signal

def signal_handle(name):
    print(f"signal_handler{name!r}")
    
event_loop = asyncio.get_event_loop()
event_loop.add_signal_handler(signal.SIGHUP, functools.partial(signal_handle, name='SIGHUP'))
event_loop.add_signal_handler(signal.SIGUSR1, functools.partial(signal_handle, name='SIGUSR1'))
event_loop.add_signal_handler(signal.SIGINT, functools.partial(signal_handle, name='SIGINT'))

async def send_signals():
    pid = os.getpid()
    print('Starting send_signal for ', pid)
    for name in ['SIGHUP', 'SIGHUP', 'SIGUSR1', 'SIGINT']:
        print('sending ', name)
        os.kill(pid, getattr(signal, name))
        # yielding control to allow the signal handler to run , 
        # since the signal does not interrupt the program flow otherwise.
        print('yielding control')
        await asyncio.sleep(0.1)
    return

try:
    event_loop.run_until_complete(send_signals())
finally:
    event_loop.close()

#%% [markdown]
# ## Combining Coroutines with Threads and Processes

#%%
import asyncio
import concurrent.futures
import logging
import sys
import time

def blocks(n):
    log = logging.getLogger(f'blocks({n})')
    log.info("running")
    time.sleep(0.1)
    log.info("done")
    return n**2

async def run_blocking_tasks(executor):
    log = logging.getLogger('run_blocking_tasks')
    log.info('starting')
    log.info('create executor tasks')
    loop = asyncio.get_event_loop()
    blocking_tasks = [loop.run_in_executor(executor, blocks, i) for i in range(6)]
    log.info('waiting executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info("results:{!r}".format(results))
    log.info("exiting")
    
logging.basicConfig(level=logging.INFO, format="%(threadName)10s %(name)18s: %(message)s", stream=sys.stderr)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(run_blocking_tasks(executor))
finally:
    event_loop.close()


#%%
import asyncio
import concurrent.futures
import logging
import sys
import time

def blocks(n):
    log = logging.getLogger(f'blocks({n})')
    log.info("running")
    time.sleep(0.1)
    log.info("done")
    return n**2

async def run_blocking_tasks(executor):
    log = logging.getLogger('run_blocking_tasks')
    log.info('starting')
    log.info('create executor tasks')
    loop = asyncio.get_event_loop()
    blocking_tasks = [loop.run_in_executor(executor, blocks, i) for i in range(6)]
    log.info('waiting executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info("results:{!r}".format(results))
    log.info("exiting")
    
logging.basicConfig(level=logging.INFO, format="%(process)10s %(name)18s: %(message)s", stream=sys.stderr)
executor = concurrent.futures.ProcessPoolExecutor(max_workers=3)
event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(run_blocking_tasks(executor))
finally:
    event_loop.close()


