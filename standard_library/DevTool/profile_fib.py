import profile
import functools


def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


def fib_seq(n):
    seq = []
    if n > 0:
        seq.extend(fib_seq(n - 1))
    seq.append(fib(n))
    return seq


@functools.lru_cache(maxsize=None)
def fib1(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib1(n - 1) + fib1(n - 2)


def fib_seq1(n):
    seq = []
    if n > 0:
        seq.extend(fib_seq1(n - 1))
    seq.append(fib1(n))
    return seq

if __name__ == '__main__':
    profile.run("print(fib_seq(20))")
    profile.run("print(fib_seq1(20))")
    profile.runctx('print(fib_seq1(n))', globals(), {'n':20})

