# Question 1
for i in range(1, 10):
    print([f"{z}*{i} = " + str(i * z) for z in range(1, i + 1)])


# Question 3
def mysort(A: list, B: list):
    return sorted(B, key=lambda x: A.index(x))


# Question 5
def _not_divisible(n):
    return lambda x: x % n > 0


def primes():
    it = (x for x in range(2, 101))
    while True:
        n = next(it)
        yield n
        it = filter(_not_divisible(n), it)


print([n for n in primes()])
