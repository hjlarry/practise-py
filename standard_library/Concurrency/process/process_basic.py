import multiprocessing
import time
import sys
import os


def slow_worker():
    print("Starting worker")
    time.sleep(0.1)
    print("Finished worker")


p = multiprocessing.Process(target=slow_worker)
print("BEFORE:", p, p.is_alive())

p.start()
print("DURING:", p, p.is_alive())

p.terminate()  # 终止进程，及其子进程
print("TERMINATED:", p, p.is_alive())

p.join()
print("JOINED:", p, p.is_alive())

print()


def exit_error():
    sys.exit(1)


def exit_ok():
    return


def return_value():
    return 1


def raises():
    raise RuntimeError("There was an error")


def terminated():
    time.sleep(3)


jobs = []
funcs = [exit_error, exit_ok, return_value, raises, terminated]
for f in funcs:
    print("Starting process for ", f.__name__)
    j = multiprocessing.Process(target=f, name=f.__name__)
    jobs.append(j)
    j.start()

jobs[-1].terminate()
for j in jobs:
    j.join()
    print(f"{j.name:>15} exitcode={j.exitcode}")


# 执行fork相当于把当前的环境变量及之后的代码拿到一个新的进程中，其之后的代码相当于在父进程和子进程都要去分别运行
# windows不能使用fork
pid = os.fork()
print("hello world")
if pid == 0:
    print(f"子进程是{os.getpid()}, 父进程是{os.getppid()}")
else:
    print(f"我是父进程 {pid}")
print()
