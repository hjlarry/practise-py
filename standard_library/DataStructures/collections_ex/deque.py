import collections
import threading
import time

print("一、 deque基础操作")
d = collections.deque("abcdefg")
print("init:", d)
print("len:", len(d))
print("head,tail: ", d[0], d[-1])
d.remove("c")
print("remove:", d)

d1 = collections.deque()
d1.extend("abcdefg")
print("extend:", d1)
d1.append("h")
print("append:", d1)
d2 = collections.deque()
d2.extendleft(range(6))
print("extendleft:", d2)
d2.appendleft(6)
print("appendleft:", d2)

print("pop:", end=" ")
d = collections.deque("abcdefg")
while True:
    try:
        print(d.pop(), end=" ")
    except IndexError:
        print()
        break
print("popleft:", end=" ")
d = collections.deque(range(6))
while True:
    try:
        print(d.popleft(), end=" ")
    except IndexError:
        print()
        break
print()

d = collections.deque(range(10))
print("init:", d)
d.rotate(2)
print("rotate(2):", d)
d.rotate(-4)
print("rotate(-4):", d)
print()

d = collections.deque(maxlen=3)
for i in range(10):
    d.append(i)
print("maxlen deque:", d)

print("二、 在多线程中使用deque")
candle = collections.deque(range(5))


def burn(direction, nextSource):
    while True:
        try:
            next = nextSource()
        except IndexError:
            break
        else:
            print(f"{direction}:{next}")
            time.sleep(0.1)
    print(f"{direction} done")
    return


left = threading.Thread(target=burn, args=("left", candle.popleft))
right = threading.Thread(target=burn, args=("right", candle.pop))
left.start()
right.start()
left.join()
right.join()
print()
