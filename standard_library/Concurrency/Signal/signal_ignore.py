import signal
import os


def do_exit(sig, stack):
    raise SystemExit("Exiting")


# 原本发送SIGINT信号相当于Ctrl+C，会引发KeyboardInterrupt，现将其忽略掉
# 并重新注册了一个信号SIGUSR1，对应引发SystemExit去退出
signal.signal(signal.SIGINT, signal.SIG_IGN)
signal.signal(signal.SIGUSR1, do_exit)
print("忽略了原本的信号SIGINT")
print("My PID:", os.getpid())
# pause相当于while true?
signal.pause()
