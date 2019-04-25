import signal
import sys
import os
import time

pid = os.getpid()
received = False


def signal_usr1(signum, frame):
    global received
    received = True
    print(f"CHILD {pid:>6}: received usr1")


print(f"CHILD {pid:>6}: setup signal handle")
sys.stdout.flush()
signal.signal(signal.SIGUSR1, signal_usr1)
print(f"CHILD {pid:>6}: pausing to wait signal")
sys.stdout.flush()
time.sleep(3)
if not received:
    print(f"CHILD {pid:>6}: never received signal")
