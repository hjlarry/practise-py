import hashlib

print("Guaranteed: \n {}".format(", ".join(sorted(hashlib.algorithms_guaranteed))))
print("Available: \n {}".format(", ".join(sorted(hashlib.algorithms_available))))
print()


lorem = """Lorem ipsum dolor sit amet, consectetur adipisicing
elit, sed do eiusmod tempor incididunt ut labore et dolore magna
aliqua. Ut enim ad minim veniam, quis nostrud exercitation
ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis
aute irure dolor in reprehenderit in voluptate velit esse cillum
dolore eu fugiat nulla pariatur. Excepteur sint occaecat
cupidatat non proident, sunt in culpa qui officia deserunt
mollit anim id est laborum."""

h1 = hashlib.md5()
h1.update(lorem.encode("utf-8"))
print(h1.hexdigest())

# 也可以用 h = hashlib.new('sha1')  传入加密方式的名称
h2 = hashlib.sha1()
h2.update(lorem.encode("utf-8"))
print(h2.hexdigest())
print()


def chunkize(size, text):
    start = 0
    while start < len(text):
        chunk = text[start : start + size]
        yield chunk
        start += size
    return


h3 = hashlib.md5()
for chunk in chunkize(64, lorem.encode("utf-8")):
    h3.update(chunk)
line_by_line = h3.hexdigest()
print("all in once:", h1.hexdigest())
print("line_by_line:", line_by_line)
print("euqal:", h1.hexdigest() == line_by_line)

