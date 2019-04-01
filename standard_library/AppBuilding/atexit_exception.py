import atexit


def exit_with_exception(msg):
    raise RuntimeError(msg)


atexit.register(exit_with_exception, "reg first")
atexit.register(exit_with_exception, "reg second")
