import threading
import signal
import time


# alarm可以在任何线程中去设置，但只能在主线程中被接收到
print("alarm在线程中的使用")


def signal_handler(num, stack):
    print(time.ctime(), "Alarm in ", threading.currentThread().name)


signal.signal(signal.SIGALRM, signal_handler)


def use_alarm():
    t_name = threading.currentThread().name
    print(time.ctime(), "Seting alarm in ", t_name)
    signal.alarm(1)
    print(time.ctime(), "Sleep in ", t_name)
    # alarm并不会终止sleep
    time.sleep(3)
    print(time.ctime(), "Done with sleep ", t_name)


alarm_thread = threading.Thread(target=use_alarm, name="alarm_thread")
alarm_thread.start()
time.sleep(0.1)

print(time.ctime(), "Wait for  ", alarm_thread.name)
alarm_thread.join()
print(time.ctime(), "Exiting normally  ")
