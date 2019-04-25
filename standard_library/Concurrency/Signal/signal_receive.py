import signal
import os
import time

print("接收信号示例:")
"""
运行后会得到当前进程的pid，再打开一个命令行运行如下命令就会发送信号
当前进程接收到信号会调用对应到处理方法
$ kill -USR1 $pid
$ kill -USR2 $pid
$ kill -INT $pid  # KeyboardInterrupt
"""


def receive_signal(signum, stack):
    print("Received:", signum)


signal.signal(signal.SIGUSR1, receive_signal)
signal.signal(signal.SIGUSR2, receive_signal)

print("My pid is ", os.getpid())
while True:
    print("wating...")
    time.sleep(3)
