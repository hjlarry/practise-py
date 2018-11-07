import timeit
import textwrap

t = timeit.Timer("print('main statement')", "print('setup')")
print("TIMEIT:")
# timeit() 执行设置语句一次，然后重复调用主语句 count 次。
print(t.timeit(2))

print("REPEAT:")
print(t.repeat(3, 2))

range_size = 1000
count = 1000
setup_statement = ";".join(["l = [(str(x), x) for x in range(1000)]", "d = {}"])


def show_results(result):
    global count, range_size
    per_pass = 1_000_000 * (result / count)
    print(f"{per_pass:6.2f} usec/pass", end=" ")
    per_item = per_pass / range_size
    print(f"{per_item:6.2f} usec/item")


print(f"{range_size} items")
print(f"{count} iterations")

print("__setitem__:")
t = timeit.Timer(
    textwrap.dedent(
        """
for s, i in l:
    d[s] = i
"""
    ),
    setup_statement,
)

show_results(t.timeit(number=count))

print("setdefault:")
t = timeit.Timer(
    textwrap.dedent(
        """
for s, i in l:
    d.setdefault(s, i)
"""
    ),
    setup_statement,
)

show_results(t.timeit(number=count))

print("keyerror:")
t = timeit.Timer(
    textwrap.dedent(
        """
for s, i in l:
    try:
        existing = d[s]
    except KeyError:
        d[s] = i
"""
    ),
    setup_statement,
)

show_results(t.timeit(number=count))

print("not in:")
t = timeit.Timer(
    textwrap.dedent(
        """
for s, i in l:
    if s not in d:
        d[s] = i
"""
    ),
    setup_statement,
)

show_results(t.timeit(number=count))
