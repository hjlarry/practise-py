from heap import MaxHeap


class PriorityQueue:
    def __init__(self, maxsize=None):
        self.maxsize = maxsize
        self._maxheap = MaxHeap(maxsize)

    def push(self, priority, value):
        self._maxheap.add((priority, value))

    def pop(self):
        entry = self._maxheap.extract()
        return entry[1]

    def is_empty(self):
        return len(self._maxheap) == 0


def test_priority_queue():
    size = 5
    pq = PriorityQueue(size)
    pq.push(5, 'purple')  # priority, value
    pq.push(0, 'white')
    pq.push(3, 'orange')
    pq.push(1, 'black')

    res = []
    while not pq.is_empty():
        res.append(pq.pop())
    assert res == ['purple', 'orange', 'black', 'white']
