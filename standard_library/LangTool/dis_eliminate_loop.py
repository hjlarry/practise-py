import operator
import itertools


class Dictionary:
    def __init__(self, words):
        self.by_letter = {}
        self.load_data(words)

    def load_data(self, words):
        # 使用itertools.groupby()可以将迭代迁移至C中
        grouped = itertools.groupby(words, key=operator.itemgetter(0))
        self.by_letter = {group[0][0]: group for group in grouped}

