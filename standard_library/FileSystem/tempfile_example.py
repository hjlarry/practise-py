import os
import tempfile
import pathlib

print("一、 创建临时文件和普通文件的区别")
# TemporaryFile创建的文件没有名称。
filename = f"/tmp/guess_name.{os.getpid()}.txt"
with open(filename, "w+b") as temp:
    print(f"temp:  {temp!r}")
    print(f"temp.name:  {temp.name!r}")
os.remove(filename)
with tempfile.TemporaryFile() as temp:
    print(f"temp:  {temp!r}")
    print(f"temp.name:  {temp.name!r}")
print()

print("二、 写入临时文件（字符串和二进制模式）")
# TemporaryFile 默认情况下文件描述符使用w+b模式打开，所以它在所有平台上行为一致
with tempfile.TemporaryFile() as temp:
    temp.write(b"some data")
    temp.seek(0)  # 写入后，将文件描述符内部指针重置到文件开始处以便读回数据
    print(temp.read())

with tempfile.TemporaryFile(mode="w+t") as temp:  # w+t表示文本模式
    temp.writelines(["some data", "some else \n", "sadsa \n"])
    temp.seek(0)
    for line in temp:
        print(line.rstrip())
print()

print("三、 命名临时文件")
# 临时文件关闭后会被删除
with tempfile.NamedTemporaryFile() as temp:
    print(f"temp:  {temp!r}")
    print(f"temp.name:  {temp.name!r}")
    f = pathlib.Path(temp.name)
print(f"Exists after close:{f.exists()}")
print()

print("四、 临时缓冲文件")
# 它在内容超过max_size之前，使用io.BytesIO或io.StringIO将数据保存在内存中
# 当内容超过max_size时，数据被写入磁盘保存，同时缓冲池被替换为TemporaryFile，也可显式调用rollover
with tempfile.SpooledTemporaryFile(max_size=1000, mode="w+t", encoding="utf-8") as temp:
    print(f"temp:  {temp!r}")
    for i in range(3):
        temp.write("this line repeat \n")
        print(temp._rolled, temp._file)
    temp.rollover()
    print(temp._rolled, temp._file)
print()

print("五、 临时目录")
with tempfile.TemporaryDirectory() as directory_name:
    the_dir = pathlib.Path(directory_name)
    print(the_dir)
    a_file = the_dir / "a.txt"
    a_file.write_text("some thing is deleted")
print("Dir exists after?", the_dir.exists())
print("Contents after?", list(the_dir.glob("*")))
print()

print("六、 设置临时文件的位置和名称")
with tempfile.NamedTemporaryFile(suffix="_suf", prefix="pre_", dir="/tmp") as temp:
    print(f"temp:  {temp!r}")
    print(f"temp.name:  {temp.name!r}")
print("gettempdir: ", tempfile.gettempdir())
print("gettempprefix: ", tempfile.gettempprefix())
tempfile.tempdir = "/Home"
print("gettempdir: ", tempfile.gettempdir())
