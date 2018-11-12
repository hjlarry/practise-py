import itertools
import operator

# 用于过滤的生成器函数
def vowel(c):
    return c.lower() in "aeiou"


print(list(filter(vowel, "HelloWorld")))
print(list(itertools.filterfalse(vowel, "HelloWorld")))

# 找到第一个返回False的元素，然后不在处理后续的元素
print(list(itertools.dropwhile(vowel, "HelloWorld")))
print(list(itertools.dropwhile(vowel, "elloWorld")))
# 返回为True的元素直到返回False则不去处理后续元素
print(list(itertools.takewhile(vowel, "HelloWorld")))
print(list(itertools.takewhile(vowel, "eeoWorld")))

print(list(itertools.compress("eeoWorld", [1, 0, 1, 0])))

print(list(itertools.islice("HelloWorld", 3)))
print(list(itertools.islice("HelloWorld", 3, 5)))
print(list(itertools.islice("HelloWorld", 3, 7, 2)))
print()

# 用于映射的生成器函数
sample = [5, 4, 2, 7, 8, 9, 1, 0, 1]
print(list(itertools.accumulate(sample)))
print(list(itertools.accumulate(sample, min)))
print(list(itertools.accumulate(sample, max)))
print(list(itertools.accumulate(sample, operator.mul)))

print(list(enumerate(sample, 2)))
print(list(map(operator.mul, sample, range(5))))
# h*2, e*3, l*4, etc..
print(list(itertools.starmap(operator.mul, enumerate("helloworld", 2))))
print()

# 用于合并的生成器函数
print(list(itertools.chain(range(5), "abc")))
print(list(itertools.chain(enumerate("abc", 2))))
print(list(itertools.chain.from_iterable(enumerate("abc", 2))))
print(list(zip(range(5), "abc", [10, 30, 40, 50])))
print(list(itertools.zip_longest(range(5), "abc", [10, 30, 40, 50])))
print(list(itertools.zip_longest(range(5), "abc", [10, 30, 40, 50], fillvalue="**")))
print()

# itertools.product()
print(list(itertools.product("abc", range(2))))
print(list(itertools.product("abc", range(2), repeat=2)))
print(list(itertools.product("abc", repeat=2)))
print()

# count, repeat, cycle
ct = itertools.count()
print(next(ct))
print(next(ct))
print(next(ct))
print(list(itertools.islice(itertools.count(1, 0.3), 5)))
print(list(itertools.islice(itertools.cycle("abc"), 5)))
print(list(itertools.repeat("abc", 5)))
# 为map的func提供相同的参数
print(list(map(operator.mul, range(10), itertools.repeat(5))))
print()

# combinations(it, out_len)，把it产出的out_len个元素组合在一起 然后产出；combinations_with_replacement会包含相同的元素
# permutations(it,out_len=None) 把out_len个it产出的元素排列在一起，然后产出这些排列
print(list(itertools.combinations("abc", 2)))
print(list(itertools.combinations("abc", 3)))
print(list(itertools.combinations_with_replacement("abc", 2)))
print(list(itertools.permutations("abc", 2)))
print(list(itertools.permutations("abc", 3)))
print()

# 重新排列元素
print(list(itertools.groupby("LLLLAALLBBB")))
for char, group in itertools.groupby("LLLLAALLBBB"):
    print(char, "->", list(group))
animals = ["duck", "rat", "bat", "bear", "lion", "shark", "dolphin"]
print(sorted(animals, key=len))
for length, group in itertools.groupby(reversed(animals), len):
    print(length, "->", list(group))

print(list(itertools.tee('abc', 3)))
g1, g2, g3 = itertools.tee('abc', 3)
print(next(g1))
print(next(g1))
print(next(g2))

