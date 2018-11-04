import os
import signal
import subprocess
import time
import pathlib

proc = subprocess.Popen("./atexit_signal_child.py")
print("Parent: pausing before sending signal")
time.sleep(1)
print("Parent: Signaling child")
os.kill(proc.pid, signal.SIGTERM)
