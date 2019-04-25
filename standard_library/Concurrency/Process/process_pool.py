import multiprocessing
import operator
import glob
import pprint
import collections
import itertools
import string
import time

print("pool example:")


def get_html(n):
    time.sleep(n)
    print("sub_process execute success")
    return n


pool = multiprocessing.Pool()
result = pool.apply_async(get_html, args=(1,))
# 等待所有任务完成
pool.close()
pool.join()
print(result.get())

new_pool = multiprocessing.Pool()
for result in new_pool.imap(get_html, [1, 5, 3]):
    print(f"{result} success")

for result in new_pool.imap_unordered(get_html, [1, 5, 3]):
    print(f"{result} success")
print()
print("buildin map and multiprocessing pool map compare")


def do_cal(data):
    return data * 2


def start_pro():
    print("Starting ", multiprocessing.current_process().name)


inputs = list(range(10))
print("Input:", inputs)
bulidin_output = map(do_cal, inputs)
print("Buildin output", bulidin_output)

pool_size = multiprocessing.cpu_count() * 2
pool = multiprocessing.Pool(
    processes=pool_size, initializer=start_pro, maxtasksperchild=2
)
pool_outputs = pool.map(do_cal, inputs)
pool.close()
pool.join()
print("Pool", pool_outputs)
print()
print("MapReduce example:")


class SimpleMapReduce:
    def __init__(self, map_func, reduce_func, num_workers=None):
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.pool = multiprocessing.Pool(num_workers)

    def partition(self, mapped_values):
        partitioned_data = collections.defaultdict(list)
        for k, v in mapped_values:
            partitioned_data[k].append(v)
        return partitioned_data.items()

    def __call__(self, inputs, chunksize=1):
        map_response = self.pool.map(self.map_func, inputs, chunksize=chunksize)
        partitioned_data = self.partition(itertools.chain(*map_response))
        reduced_values = self.pool.map(self.reduce_func, partitioned_data)
        return reduced_values


def file_to_words(filename):
    STOP_WORDS = set(
        [
            "a",
            "an",
            "and",
            "are",
            "as",
            "be",
            "by",
            "for",
            "if",
            "in",
            "is",
            "it",
            "of",
            "or",
            "py",
            "rst",
            "that",
            "the",
            "to",
            "with",
        ]
    )
    TR = str.maketrans({p: " " for p in string.punctuation})
    print(f"{multiprocessing.current_process().name} reading {filename}")
    output = []
    with open(filename, "rt") as f:
        for line in f:
            if line.lstrip().startswith(".."):
                continue
            line = line.translate(TR)
            for word in line.split():
                word = word.lower()
                if word.isalpha() and word not in STOP_WORDS:
                    output.append((word, 1))
    return output


def count_words(item):
    word, ouucrences = item
    return (word, sum(ouucrences))


inputs = glob.glob("*.py")
mapper = SimpleMapReduce(file_to_words, count_words)
word_counts = mapper(inputs)
word_counts.sort(key=operator.itemgetter(1))
word_counts.reverse()

print("TOP 20 WORD")
top20 = word_counts[:20]
pprint.pprint(top20)
