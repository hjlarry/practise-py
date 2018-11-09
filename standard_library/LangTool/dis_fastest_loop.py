import collections


class Dictionary:
    def __init__(self, words):
        self.by_letter = collections.defaultdict(list)
        self.load_data(words)

    def load_data(self, words):
        # 观察字节码by_letter会少一个操作指令
        by_letter = self.by_letter
        for word in words:
            by_letter[word[0]].append(word)
