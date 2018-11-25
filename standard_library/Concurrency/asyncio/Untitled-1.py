

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


