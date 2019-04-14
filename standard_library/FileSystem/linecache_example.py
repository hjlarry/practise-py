import os
import tempfile
import linecache
import this

lorem = """Lorem ipsum dolor sit amet, consectetuer
adipiscing elit.  Vivamus eget elit. In posuere mi non
risus. Mauris id quam posuere lectus sollicitudin
varius. Praesent at mi. Nunc eu velit. Sed augue massa,
fermentum id, nonummy a, nonummy sit amet, ligula. Curabitur
eros pede, egestas at, ultricies ac, apellentesque eu,
tellus.

Sed sed odio sed mi luctus mollis. Integer et nulla ac augue
convallis accumsan. Ut felis. Donec lectus sapien, elementum
nec, condimentum ac, interdum non, tellus. Aenean viverra,
mauris vehicula semper porttitor, ipsum odio consectetuer
lorem, ac imperdiet eros odio a sapien. Nulla mauris tellus,
aliquam non, egestas a, nonummy et, erat. Vivamus sagittis
porttitor eros."""


def make_tempfile():
    fd, temp_file_name = tempfile.mkstemp()
    os.close(fd)
    with open(temp_file_name, "wt") as f:
        f.write(lorem)
    return temp_file_name


def cleanup(filename):
    os.unlink(filename)


filename = make_tempfile()
nl = "\n"
# 从源文件和缓存中挑出相同的行
# linecache从第一行开始计数，返回的每行都包含一个换行符
print("Source:")
print(f"{lorem.split(nl)[4]!r}")
print("Cache:")
print(f"{linecache.getline(filename, 5)!r}")
# 空行就返回换行符
print(f"Blank: {linecache.getline(filename, 8)!r}")
# 返回空字符串则这行不存在
print(f"NotThere: {linecache.getline(filename, 500)!r}")
# 文件不存在时也不会引发错误
print(f"FileNotExist: {linecache.getline('not_exist_file_9', 500)!r}")
print()
# 会在sys.path中搜寻this.py
module_line = linecache.getline("this.py", 3)
print("Module:")
print(repr(module_line))
print(module_line)
# 通过文件读取的方式获取file_line
file_src = this.__file__
if file_src.endswith("pyc"):
    file_src = file_src[:-1]  # 找this.py
with open(file_src, "r") as f:
    file_line = f.readlines()[2]
print(repr(file_line))
