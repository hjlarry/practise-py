import random


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
