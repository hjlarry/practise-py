import collections

Result = collections.namedtuple("Result", "count average")


def average():
    total = 0
    count = 0
    average = None
    while True:
        recv = yield average
        if recv is None:
            break
        total += recv
        count += 1
        average = total / count
    return Result(count, average)


avg_cor = average()
next(avg_cor)
print(avg_cor.send(100))
print(avg_cor.send(50))
print(avg_cor.send(10))
# print(avg_cor.send(None))
try:
    avg_cor.send(None)
except StopIteration as e:
    result = e.value
print(result)