import logging
import threading
import time

def daemon():
    logging.debug('Daemon Starting')
    time.sleep(0.2)
    logging.debug('Daemon Exit')
    
def non_daemon():
    logging.debug('Starting')
    logging.debug('Exit')
    

# import random
#
# def worker():
#     pause = random.randint(1,5)/10
#     logging.debug('Daemon Starting sleep %0.2f', pause)
#     time.sleep(pause)
#     logging.debug('Daemon Exit')
#
# logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] (%(threadName)-10s) %(message)s")
# for i in range(3):
#     t = threading.Thread(target=worker, daemon=True)
#     t.start()
#
# main_thread = threading.main_thread()
#
# print(threading.enumerate())
#
# for t in threading.enumerate():
#     if t is main_thread:
#         continue
#     logging.debug('%s joining' , t.getName())
#     t.join()

import subprocess
cat = subprocess.Popen(['cat', 'Concurrency/signal.ipynb'], stdout=subprocess.PIPE)
grep = subprocess.Popen(['grep', 'def'],stdin=cat.stdout, stdout=subprocess.PIPE)
cut = subprocess.Popen(['cut', '-b', '-30'],stdin=grep.stdout, stdout=subprocess.PIPE)
end_of_pipe = cut.stdout

print('Included files:')
for line in end_of_pipe:
    print(line)

import string
import os

os.system('pwd')
# import sys

# workers = []
# for i in range(2):
#     print(f"Parent {os.getpid()} : Forking {i}")
#     worker_pid = os.fork()
#     if not worker_pid:
#         print(f"Worker {i} starting")
#         time.sleep(2+i)
#         print(f"Worker {i} finish")
#         sys.exit(i)
#     workers.append(worker_pid)

# for pid in workers:
#     print('Parent waiting for pid', pid)
#     done = os.waitpid(pid,0)
#     print('Parent child done ', done)

os.spawnlp(os.P_WAIT, 'pwd', 'pwd', '-P')