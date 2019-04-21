"""

整个运行流程如下:

父进程实例化 Popen；
 Popen 实例 fork 新进程；
新进程运行 os.setpgrp()；
新进程运行exec() 启动 shell；
shell 运行脚本；
shell 脚本再次 fork，然后启动 Python 解释器；
Python 运行 signal_child.py.
父进程发送信号至进程组，使用 Popen 实例的进程id；
shell and Python 程序收到信号；
shell 忽略掉了信号。
运行 signal_child.py 的 Python 程序 调用了信号处理器。
"""


import os
import signal
import subprocess
import tempfile
import time
import sys

print("使用进程组可以解决subprocess_signal_parent_shell的signal_child无法接收到信号的问题")


def show_setting_prgrp():
    os.setpgrp()


script = """#!/bin/sh
echo "Shell script in process $$"
set -x
python3 signal_child.py
"""

script_file = tempfile.NamedTemporaryFile("wt")
script_file.write(script)
script_file.flush()

proc = subprocess.Popen(["sh", script_file.name], preexec_fn=show_setting_prgrp)
print(f"Parent: Pausing before signal {proc.pid}")
sys.stdout.flush()
time.sleep(1)
print(f"Parent: Signaling child {proc.pid}")
sys.stdout.flush()
os.killpg(proc.pid, signal.SIGUSR1)
time.sleep(3)
