import os
import signal
import time
import sys
import subprocess

print("父进程向子进程发送信号，子进程会接收到信号")
proc = subprocess.Popen(["python3", "signal_child.py"])
print("PARENT: Pausing before sending signal")
sys.stdout.flush()
time.sleep(1)
print("PARENT: Signaling child")
sys.stdout.flush()
os.kill(proc.pid, signal.SIGUSR1)
