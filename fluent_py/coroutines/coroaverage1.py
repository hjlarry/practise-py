from coroutil import coroutine

@coroutine
def average():
    total = 0
    count = 0
    average = None
    while True:
        recv = yield average
        total += recv
        count += 1
        average = total / count

avg_cor = average()
print(avg_cor.send(100))
print(avg_cor.send(50))
print(avg_cor.send(10))
print(avg_cor.send(0))
