# 固定长度数组实现
class Array:
    def __init__(self, size=32):
        self._size = size
        self._item = [None] * self._size

    def __getitem__(self, index):
        return self._item[index]

    def __setitem__(self, index, value):
        self._item[index] = value

    def __len__(self):
        return self._size

    def clear(self):
        for i in range(len(self)):
            self[i] = None

    def __iter__(self):
        for item in self._item:
            yield item


def test_array():
    a = Array()
    assert len(a) == 32

    a[3] = 5
    assert a[3] == 5

    a.clear()
    assert a[3] is None
