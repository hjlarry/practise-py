import glob
import shutil
import io
import pathlib
import os
import pprint
import logging
import sys
import tarfile
import tempfile

CURRENT_DIR = pathlib.Path(__file__).parent
print("一、 复制文件")
shutil.copyfile(
    CURRENT_DIR / "test_files/example.txt", CURRENT_DIR / "test_files/example.txt.copy"
)


class VerboseStringIO(io.StringIO):
    def read(self, n=-1):
        next = super().read(n)
        print(f"read({n}) got {len(next)} bytes")
        return next


lorem_ipsum = """Lorem ipsum dolor sit amet, consectetuer
adipiscing elit.  Vestibulum aliquam mollis dolor. Donec
vulputate nunc ut diam. Ut rutrum mi vel sem. Vestibulum
ante ipsum."""

# copyfile() 不管文件的类型如何，都会打开进行读取，一些特殊的文件（例如 Unix 设备）是不能使用它进行复制的。
# copyfile() 使用低级的方法 copyfileobj() 实现。
# 传入 copyfile() 的参数是文件名称，而传入 copyfileobj() 是打开的文件描述符。
# 可选的第三个参数用来设置读取块的大小。 -1表示一次性全部读取。
print("All at once:")
input = VerboseStringIO(lorem_ipsum)
output = io.StringIO()
shutil.copyfileobj(input, output, -1)
print("Block 256:")
input = VerboseStringIO(lorem_ipsum)
output = io.StringIO()
shutil.copyfileobj(input, output, 128)
print("Before:", glob.glob("test_files/test/*"))
shutil.copy("test_files/example.txt", "test_files/test")
print("After:", glob.glob("test_files/test/*"))
print()

print("二、 处理目录树")
print("Before:")
pprint.pprint(glob.glob("/tmp/example_dir/*"))
shutil.copytree("test_files/test", "/tmp/example_dir")
print("After:")
pprint.pprint(glob.glob("/tmp/example_dir/*"))
shutil.rmtree("/tmp/example_dir")

print("BEFORE: ", glob.glob("test_files/example*"))
# 原理类似于 Unix 命令 mv 。如果源文件和目标文件都存在，源文件将会被重命名。否则源文件被复制到目的地然后被删除。
shutil.move("test_files/example.txt", "test_files/example.out")
print("AFTER : ", glob.glob("test_files/example*"))
# 恢复
shutil.move("test_files/example.out", "test_files/example.txt")
print()

print("三、 查找文件")
print(shutil.which("virtualenv"))
print(shutil.which("tox"))
print(shutil.which("git"))
print(shutil.which("io_example.py"))
print(shutil.which("python3"))

path = os.pathsep.join([".", os.path.expanduser("~")])
mode = os.F_OK | os.R_OK
# path 参数默认是 os.environ('PATH')，但是可以是任何由 os.pathsep 分隔的字符串
filename = shutil.which("jmeter.log", mode=mode, path=path)
print(path)
print(filename)
print()

print("四、 压缩文件")
for format, des in shutil.get_archive_formats():
    print(f"{format:>5}  {des}")

for format, ends, des in shutil.get_unpack_formats():
    print(f"{format :>5} {str(ends): <25} {des}")

logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("pymotw")
print("Creating archive:")
shutil.make_archive(
    "test_files/example", "gztar", root_dir=".", base_dir="test_files", logger=logger
)
print("\nArchive contents:")
with tarfile.open("test_files/example.tar.gz", "r") as t:
    for n in t.getnames():
        print(n)

with tempfile.TemporaryDirectory() as d:
    print("Unpacking archive:", end=" ")
    shutil.unpack_archive("test_files/example.tar.gz", extract_dir=d)
    print("\nCreated:")
    prefix_len = len(d) + 1
    for extracted in pathlib.Path(d).rglob("*"):
        print(str(extracted))
        print(str(extracted)[prefix_len:])
print()

print("五、文件系统空间")
total_b, used_b, free_b = shutil.disk_usage(".")
gib = 2 ** 30  # GiB == gibibyte
gb = 10 ** 9  # GB == gigabyte

print(f"Total: {total_b/gb :6.2f} GB {total_b/gib :6.2f} GiB")
print(f"Used: {used_b/gb :6.2f} GB {used_b/gib :6.2f} GiB")
print(f"Free: {free_b/gb :6.2f} GB {free_b/gib :6.2f} GiB")
