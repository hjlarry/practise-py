import mmap
import shutil
import re

"""
内存映射一个文件并不会导致整个文件被读取到内存中。 也就是说，文件并没有被复制到内存缓存或数组中。
相反，操作系统仅仅为文件内容保留了一段虚拟内存。 当你访问文件的不同区域时，这些区域的内容才根据需要被读取并映射到内存区域中。 
而那些从没被访问到的部分还是留在磁盘上。 所以，内存映射通常可以提高 I/O 性能。
"""
print("一、 读取")
with open("test_files/lorem.txt", "r") as f:
    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
        print("First 10 bytes via read:", m.read(10))
        print("First 10 bytes via slice:", m[:10])
        print("2nd 10 bytes via read:", m.read(10))
print()

print("二、 写入(复制原文件并更改一个单词来观察前后变化)")
shutil.copyfile("test_files/lorem.txt", "test_files/lorem_copy.txt")
word = b"consectetuer"
reversed = word[::-1]
print("looking for ", word)
print("replacing for ", reversed)
with open("test_files/lorem_copy.txt", "r+") as f:
    with mmap.mmap(f.fileno(), 0) as m:
        print(f"Before:{m.readline().rstrip()}")
        m.seek(0)

        loc = m.find(word)
        m[loc : loc + len(word)] = reversed
        m.flush()

        m.seek(0)
        print(f"After:{m.readline().rstrip()}")

        f.seek(0)
        print(f"File:{f.readline().rstrip()}")
print()


print("三、 复制模式下写入")
shutil.copyfile("test_files/lorem.txt", "test_files/lorem_copy.txt")
word = b"consectetuer"
reversed = word[::-1]
print("looking for ", word)
print("replacing for ", reversed)
with open("test_files/lorem_copy.txt", "r+") as f:
    # 采用写入模式时，文件和mmap都会被修改；而复制模式，文件并没有被修改
    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_COPY) as m:
        print(f"Before:{m.readline().rstrip()}")
        print(f"File Before:{f.readline().rstrip()}")
        m.seek(0)

        loc = m.find(word)
        m[loc : loc + len(word)] = reversed
        m.flush()

        m.seek(0)
        print(f"After:{m.readline().rstrip()}")

        f.seek(0)
        print(f"File After:{f.readline().rstrip()}")
print()

print("四、 使用正则匹配")
pattern = re.compile(
    rb"(\.\W+)?([^.]?nulla[^.]*?\.)", re.DOTALL | re.IGNORECASE | re.MULTILINE
)
with open("test_files/lorem.txt", "r") as f:
    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
        for match in pattern.findall(m):
            print(match[1].replace(b"\n", b" "))
