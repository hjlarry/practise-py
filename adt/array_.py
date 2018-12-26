# 固定长度数组实现
class Array:
    def __init__(self, size=32):
        self._size = size
        self._item = []

    def __getitem__(self, index):
        return self._item[index]

    def __setitem__(self, index, value):
        self._item[index] = value

    def __len__(self):
        return len(self._item)

    def clear(self):
        for i in range(len(self)):
            self[i] = None

    def __iter__(self):
        for item in self._item:
            yield item

    def find(self, index):
        try:
            return self._item[index]
        except IndexError:
            return None

    def delete(self, index):
        try:
            self._item.pop(index)
            return True
        except IndexError:
            return False

    def insert(self, index, value):
        if len(self) >= self._size:
            return False
        else:
            return self._item.insert(index, value)

    def print_all(self):
        for item in self:
            print(item)


def test_array():
    array = Array(5)
    array.insert(0, 3)
    array.insert(0, 4)
    array.insert(1, 5)
    array.insert(3, 9)
    array.insert(3, 10)
    assert array.insert(0, 100) is False
    assert len(array) == 5
    array.print_all()
    assert array.find(1) == 5
    assert array.delete(4) is True
    array.print_all()
    array.clear()
    assert array[3] is None


if __name__ == "__main__":
    test_array()
