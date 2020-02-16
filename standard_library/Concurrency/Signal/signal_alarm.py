import time
import signal

# 警报是一种特殊的信号，程序要求操作系统在一段时间之后再去通知它。


def receive_alarm(signum, stack):
    print(signum)
    time.sleep(1)
    print("Alarm :", time.ctime())


print("警报使用示例")
signal.signal(signal.SIGALRM, receive_alarm)
signal.alarm(2)
print("Before:", time.ctime())
time.sleep(6)  # 调用过程中信号进入执行
print("After:", time.ctime())
