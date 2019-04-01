import collections
import itertools
import multiprocessing
import operator


class SimpleMapReduce:
    def __init__(self, map_func, reduce_func, num_workers=None):
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.pool = multiprocessing.Pool(num_workers)

    def partition(self, mapped_values):
        partitioned_data = collections.defaultdict(list)
        for key, value in mapped_values:
            partitioned_data[key].append(value)
        return partitioned_data.items()

    def __call__(self, inputs, chunksize=1):
        map_responses = self.pool.map(self.map_func, inputs, chunksize=chunksize)
        partitioned_data = self.partition(itertools.chain(*map_responses))
        reduced_values = self.pool.map(self.reduce_func, partitioned_data)
        return reduced_values


def file_to_words(filename):
    print("{} reading {}".format(multiprocessing.current_process().name, filename))

    output = []
    words = []
    with open("chinese_words.txt", "rb") as d:
        for line in d:
            words.append(line.decode("gbk").strip())
    with open(filename, "rb") as f:
        for line in f:
            for word in words:
                if word in line.decode():
                    output.append((word, 1))
    return output


def count_words(item):
    word, occurences = item
    return (word, sum(occurences))


input_files = ["xiaoshuo1.txt", "xiaoshuo2.txt", "xiaoshuo3.txt"]
mapper = SimpleMapReduce(file_to_words, count_words)
word_counts = mapper(input_files)
word_counts.sort(key=operator.itemgetter(1))

print("\nTOP 20 WORDS BY FREQUENCY\n")
top20 = word_counts[-20:]
longest = max(len(word) for word, count in top20)
for word, count in top20:
    print("{word:<{len}}: {count:5}".format(len=longest + 1, word=word, count=count))
