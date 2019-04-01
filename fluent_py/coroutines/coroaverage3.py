import collections

Result = collections.namedtuple("Result", "count average")
# main()是调用方， grouper()是委托生成器，average()是子生成器
# yield from会在调用方和子生成器之间建立一个双向通道


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


def grouper(results, key):
    while True:
        results[key] = yield from average()


def main(data):
    results = {}
    for k, values in data.items():
        group = grouper(results, k)
        next(group)  # 预激
        for value in values:
            group.send(value)
        group.send(None)
    print(results)


data = {
    "girls;kg": [40.9, 45.1, 44.3, 33.4],
    "girls;m": [1.63, 1.71, 1.82, 1.59],
    "boys;kg": [60, 71.2, 80],
}

main(data)
