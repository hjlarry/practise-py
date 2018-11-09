import dis


def f(*args):
    return len(args)


dis.show_code(f)

i = 1
j = 0

try:
    result = i / j
except Exception:
    import sys

    exc_type, exc_value, exc_tb = sys.exc_info()
    dis.distb(exc_tb)

