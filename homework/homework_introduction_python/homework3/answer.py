# Question 1
class Prime:
    def __init__(self, max):
        self.v = 2
        self.max = max

    def __iter__(self):
        return self

    def __next__(self):
        prime = self.v
        if prime > self.max:
            raise StopIteration
        self.v += 1
        for i in range(2, self.v-1):
            if prime % i == 0:
                return next(self)
        return prime


# Question 2
def prime(limit):
    prime_list = [2]
    v = 3
    while True:
        for i in prime_list:
            if v % i == 0:
                break
        else:
            if len(prime_list) <= limit:
                prime_list.append(v)
                yield v
            else:
                raise StopIteration
        v += 2


# Question 3
from itertools import islice, cycle
def roundrobin(*iterables):
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))