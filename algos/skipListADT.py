import random

random.seed(1)


class SkiplistNode:
    def __init__(self, value=None, max_level=None):
        self.value, self.max_level = value, max_level
        self.forwards = []

    def __repr__(self):
        return f"<data:{self.value}, level:{self.max_level}>"


class Skiplist:
    def __init__(self, max_level=16):
        self.level_count = 1
        self.max_level = max_level
        self.head = SkiplistNode()
        self.head.forwards = [None] * self.max_level

    def _get_random_level(self, p=0.5):
        level = 1
        while random.random() < p and level < self.max_level:
            level += 1
        return level

    def insert(self, value):
        level = self._get_random_level()
        new_node = SkiplistNode(value=value, max_level=level)
        new_node.forwards = [None] * level
        update = [self.head] * level
        # record every level largest value which smaller than insert value in update[]
        p = self.head
        for i in range(level - 1, -1, -1):
            while p.forwards[i] and p.forwards[i].value < value:
                p = p.forwards[i]
            update[i] = p  # use update save node in search path
        # in search path node next node become new node forwords(next)
        for i in range(level):
            new_node.forwards[i] = update[i].forwards[i]
            update[i].forwards[i] = new_node
        # update node hight
        if self.level_count < level:
            self.level_count = level

    def find(self, value):
        p = self.head
        for i in range(self.level_count - 1, -1, -1):
            while p.forwards[i] and p.forwards[i].value < value:
                p = p.forwards[i]
        if p.forwards[0] and p.forwards[0].value == value:
            return p.forwards[0]
        return False

    def delete(self, value):
        update = [None] * self.level_count
        p = self.head
        for i in range(self.level_count - 1, -1, -1):
            while p.forwards[i] and p.forwards[i].value < value:
                p = p.forwards[i]
            update[i] = p
        if p.forwards[0] and p.forwards[0].value == value:
            for i in range(self.level_count - 1, -1, -1):
                if update[i].forwards[i] and update[i].forwards[i].value == value:
                    update[i].forwards[i] = update[i].forwards[i].forwards[i]

    def __repr__(self):
        values = []
        p = self.head
        while p.forwards[0]:
            values.append(str(p.forwards[0]))
            p = p.forwards[0]
        return "->".join(values)


def test_skiplist():
    sl = Skiplist()
    for i in range(20):
        sl.insert(i)
    print(sl)
    for i in range(20):
        p = sl.find(i)
        print(p.forwards)
    sl.delete(10)
    assert sl.find(10) is False


if __name__ == "__main__":
    test_skiplist()
