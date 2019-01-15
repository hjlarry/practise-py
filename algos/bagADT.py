class Bag:
    def __init__(self, size=10):
        self.size = size
        self.data = set()

    def add(self, item):
        if len(self) < self.size:
            self.data.add(item)
        else:
            raise Exception

    def remove(self, item):
        self.data.remove(item)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for item in self.data:
            yield item


def test_bag():
    bag = Bag()
    bag.add(1)
    bag.add(2)
    bag.add(3)
    bag.add(4)

    assert len(bag) == 4

    bag.remove(2)
    assert len(bag) == 3

    for i in bag:
        print(i)


if __name__ == "__main__":
    test_bag()
