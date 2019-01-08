import collections
import threading
import time

d = collections.deque("abcdefg")
print(d)
print(len(d))
print(d[0], d[-1])
d.remove("c")
print(d)
print()

d1 = collections.deque()
d1.extend("abcdefg")
print(d1)
d1.append("h")
print(d1)
d2 = collections.deque()
d2.extendleft(range(6))
print(d2)
d2.appendleft(6)
print(d2)
print()

print("POP:")
d = collections.deque("abcdefg")
while True:
    try:
        print(d.pop(), end=" ")
    except IndexError:
        print()
        break
print("POPLEFT:")
d = collections.deque(range(6))
while True:
    try:
        print(d.popleft(), end=" ")
    except IndexError:
        print()
        break
print()


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


d = collections.deque(range(10))
print(d)
d.rotate(2)
print(d)
d.rotate(-4)
print(d)
print()

d = collections.deque(maxlen=3)
for i in range(10):
    d.append(i)
print(d)
