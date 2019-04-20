"""
用于发送信号的 pid 与等待信号的运行 shell 脚本的子进程 id 不同，因为这个例子中有三个独立的进程在交互：

1. 主程序 subprocess_signal_parent_shell.py
2. 主程序创建的运行脚本的 shell 进程。
3. 程序signal_child.py

如果由 Popen 创建的进程产生子进程，那么子进程将不会收到任何发送给父进程的任何信号。
"""

import os
import signal
import subprocess
import tempfile
import time
import sys

script = """#!/bin/sh
echo "Shell script in process $$"
set -x
python3 signal_child.py
"""

script_file = tempfile.NamedTemporaryFile("wt")
script_file.write(script)
script_file.flush()

proc = subprocess.Popen(["sh", script_file.name])
print(f"Parent: Pausing before signal {proc.pid}")
sys.stdout.flush()
time.sleep(1)
print(f"Parent: Signaling child {proc.pid}")
sys.stdout.flush()
os.kill(proc.pid, signal.SIGUSR1)
time.sleep(3)
