class LookingGlass:
    def __enter__(self):
        import sys

        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return "JABBAWOCKY"

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback):
        import sys

        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print("do not dived by zero!")
            return True


with LookingGlass() as lg:
    print("hello world!")
    print(lg)
    print(1 / 0)
print(lg)
print()


manager = LookingGlass()
monster = manager.__enter__()
print(monster)
print(monster == "JABBAWOCKY")
manager.__exit__(None, None, None)
print(monster)
