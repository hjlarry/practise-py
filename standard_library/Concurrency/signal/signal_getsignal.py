import signal


def alarm_received(n, stack):
    return


# 对某个信号重新注册一个处理器，会反应在下面的输出结果中
signal.signal(signal.SIGALRM, alarm_received)

print("输出所有注册了的signal:")
signals_to_names = {
    getattr(signal, n): n for n in dir(signal) if n.startswith("SIG") and "_" not in n
}
"""
使用 getsignal() 函数可以查看某个信号注册了哪个信号处理器。
传入信号编号作为参数，返回值是注册的信号处理器，或者特殊值 SIG_IGN （如果信号被忽略），SIG_DFL（默认信号处理行为），或者 None （如果存在的信号处理器是从 C 注册的）。
发送信号的函数是os.kill()。
"""
for s, name in sorted(signals_to_names.items()):
    handler = signal.getsignal(s)
    if handler is signal.SIG_DFL:
        handler = "SIG_DFL"
    elif handler is signal.SIG_IGN:
        handler = "SIG_IGN"
    print(f"{name:<10} ({s:2d}) :", handler)
