import contextlib


@contextlib.contextmanager
def looking_glass():
    import sys

    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    yield "JABBAWOCKY"
    sys.stdout.write = original_write


@contextlib.contextmanager
def looking_glass_exc():
    import sys

    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ""
    try:
        yield "JABBAWOCKY"
    except ZeroDivisionError:
        msg = "do not dived by zero"
    finally:
        sys.stdout.write = original_write
        print(msg)


with looking_glass_exc() as lg:
    print("hello world!")
    print(lg)
    print(1 / 0)
print(lg)
print()


manager = looking_glass()
monster = manager.__enter__()
print(monster)
print(monster == "JABBAWOCKY")
manager.__exit__(None, None, None)
print(monster)
