import atexit
import time
import sys


def not_called():
    print("child: atexit handler should not been called")


print("Child: registering atexit handler")
sys.stdout.flush()
atexit.register(not_called)

print("Child: pausing to wait for signal")
sys.stdout.flush()
time.sleep(5)
