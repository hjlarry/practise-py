import threading
import itertools
import sys
import time


class Signal:
    go = True


def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle("|/-\\"):
        status = char + " " + msg
        write(status)
        flush()
        # 使用退格符移回光标
        write("\x08" * len(status))
        time.sleep(0.1)
        if not signal.go:
            break
    write(" " * len(status) + "\x08" * len(status))


def slow_function():
    # 假装io等待
    time.sleep(3)
    return 42


def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin, args=("thinking", signal))
    print("spinner obj", spinner)
    spinner.start()
    result = slow_function()
    signal.go = False
    spinner.join()
    return result


result = supervisor()
print("Answer:", result)
