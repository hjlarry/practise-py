import threading
import signal
import time
import os

"""
信号和线程通常不会很好结合在一起，因为只有进程的主线程才会接受信号。
下例尝试在一个线程中等待信号到达，然后从另一个线程中发送信号。
尽管接收线程调用了 signal.pause()，但是它不会接收到信号。
脚本结束位置的 signal.alarm(2) 阻止了无限循环，否则接收者线程永远不会退出。
"""

print("信号在子线程中无法接收到")


def signal_handler(num, stack):
    print(f"Receive signal {num} in {threading.currentThread().name}")


signal.signal(signal.SIGUSR1, signal_handler)


def wait_for_signal():
    print("Wait for signal in ", threading.currentThread().name)
    signal.pause()
    print("Done waiting")


# 启动一个不会接收信号的线程
receiver = threading.Thread(target=wait_for_signal, name="receiver")
receiver.start()
time.sleep(0.1)


def send_signal():
    print("Sending signal in ", threading.currentThread().name)
    os.kill(os.getpid(), signal.SIGUSR1)


sender = threading.Thread(target=send_signal, name="sender")
sender.start()
sender.join()

# 等待线程看到信号（不会发生）
print("Waiting for ", receiver.name)
signal.alarm(2)
receiver.join()
