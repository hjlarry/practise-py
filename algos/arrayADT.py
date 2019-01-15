# 固定长度数组实现
class Array:
    def __init__(self, size=32, init=None):
        self._size = size
        self._items = [init] * size

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"{self.__class__}[{','.join(list(str(item) for item in self))}]"

    def clear(self):
        for i in range(len(self)):
            self[i] = None

    def __iter__(self):
        for item in self._items:
            if item:
                yield item

    def find(self, index):
        try:
            return self._items[index]
        except IndexError:
            return None

    def delete(self, index):
        try:
            self._items.pop(index)
            self._items.append(None)  # 保持固定长度
            return True
        except IndexError:
            return False

    def insert(self, index, value):
        if None in self._items:
            self._items.insert(index, value)
            self._items.pop()
            return True
        else:
            return False

    def print_all(self):
        print(self)


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
