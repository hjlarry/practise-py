from array_ import Array


class ArrayQueue:
    def __init__(self, n):
        self.items = Array(n)
        self.n = n
        self.head = 0
        self.tail = 0

    def enqueue(self, item):
        if self.tail == self.n:  # 说明队列末尾没有空间
            if self.head == 0:  # 说明队列满了
                return False
            # 进行数据搬移
            new_items = Array(self.n)
            for i in range(self.head, self.tail):
                new_items.insert(i - self.head, self.items[i])
            # 搬移后更新 head 和 tail
            self.tail -= self.head
            self.head = 0
            self.items = new_items

        self.items.insert(self.tail, item)
        self.tail += 1
        return True

    def dequeue(self):
        if self.head == self.tail:
            return None
        item = self.items[self.head]
        self.head += 1
        return item


def test_arrayqueue():
    a = ArrayQueue(5)
    a.enqueue(1)
    a.enqueue(2)
    a.enqueue(3)
    a.enqueue(4)
    a.enqueue(5)

    assert a.dequeue() == 1
    assert a.dequeue() == 2
    a.enqueue(6)
    print(a.items)


# 循环队列可以避免数据搬移
class CircularQueue:
    def __init__(self, n):
        self.items = Array(n + 1)
        self.n = n + 1
        self.head = 0
        self.tail = 0

    def enqueue(self, item):
        # 判断队列满的公式是总结规律得出的
        if (self.tail + 1) % self.n == self.head:
            return False
        self.items[self.tail] = item
        self.tail = (self.tail + 1) % self.n
        return True

    def dequeue(self):
        if self.head == self.tail:
            return None
        item = self.items[self.head]
        self.head = (self.head + 1) % self.n
        return item


def test_circlequeue():
    a = CircularQueue(5)
    a.enqueue(1)
    a.enqueue(2)
    a.enqueue(3)
    a.enqueue(4)
    a.enqueue(5)

    assert a.dequeue() == 1
    assert a.dequeue() == 2
    a.enqueue(6)
    a.enqueue(7)
    print(a.items)
    assert a.dequeue() == 3
    a.enqueue(8)
    assert a.dequeue() == 4
    assert a.dequeue() == 5
    assert a.dequeue() == 6
    assert a.dequeue() == 7
    assert a.dequeue() == 8


if __name__ == "__main__":
    test_arrayqueue()
    test_circlequeue()
