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
            for i in range(self.head, self.tail):
                self.items[i - self.head] = self.items[i]
            # 搬移后更新 head 和 tail
            self.tail -= self.head
            self.head = 0

        self.items[self.tail] = item
        self.tail += 1
        return True

    def dequeue(self):
        if self.head == self.tail:
            return None
        item = self.items[self.head]
        self.head += 1
        return item


# 循环队列可以避免数据搬移
class CircularQueue:
    def __init__(self, n):
        self.items = Array(n)
        self.n = n
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
