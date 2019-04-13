import os
import time
import os.path

print(os.path.__file__)

PATHS = ["/one/two/three", "/one/two/three/", "/", ".", ""]
print("一、 路径解析")
# split()函数返回结果的第一部分的值是dirname()函数，第二部分是basename()
print("os.path.split():")
for path in PATHS:
    print("{!r:>20} : {}".format(path, os.path.split(path)))
print("os.path.basename():")
for path in PATHS:
    print(f"{path !r:>20} : {os.path.basename(path)}")
print("os.path.dirname():")
for path in PATHS:
    print(f"{path !r:>20} : {os.path.dirname(path)}")


PATHS = [
    "filename.txt",
    "filename",
    "/path/to/filename.txt",
    "/",
    "",
    "my-archive.tar.gz",
    "no-extension.",
]
print("os.path.splitext():")
for path in PATHS:
    print(f"{path !r:>30} : {os.path.splitext(path)}")

paths = ["/one/two/three/four", "/one/two/threefold", "/one/two/three/"]
print("commonprefix()获取公共路径前缀:", os.path.commonprefix(paths))
print("commonpath()获取公共有效子路径:", os.path.commonpath(paths))
print()

print("二、 路径构建")
PATHS = [
    ("one", "two", "three"),
    ("/", "one", "two", "..t.hree"),
    # 如果某个参数以 / 开头，那么其前面的参数都会被舍弃
    ("/one", "/two", "three"),
]
print("os.path.join():")
for path in PATHS:
    print(f"{path !r:>35} : {os.path.join(*path)}")

# expanduser() 将会转化波浪号（~）为用户主目录的名称，如果没找到，会字符串原样返回
print("os.path.expanduser():")
for user in ["", "hejl", "nosuchuser"]:
    lookup = "~" + user
    print(f"{lookup!r:>15} : {os.path.expanduser(lookup)!r}")

os.environ["MYVAR"] = "TESTVALUE"
# expandvars()会解析路径中所有 shell 环境变量。
print("os.path.expandvars():", os.path.expandvars("/path/to/$MYVAR"))
print()
print("三、 规范路径")
PATHS = ["one//two//three", "one/./two/./three", "one/../alt/two/three"]
# 使用 os.normpath() 可以清理由os.curdir(指.)和os.pardir(指..)组成的路径片段
print("os.path.normpath():")
for path in PATHS:
    print(f"{path!r:>22} : {os.path.normpath(path)!r}")

os.chdir("/Users/hejl")
PATHS = [".", "..", "./one/two/three", "../one/two/three"]
print("os.path.abspath():")
for path in PATHS:
    print(f"{path!r:>21} : {os.path.abspath(path)!r}")
print()
print("四、 文件操作")
print("File         :", __file__)
print("Access time  :", time.ctime(os.path.getatime(__file__)))
print("Modified time:", time.ctime(os.path.getmtime(__file__)))
print("Change time  :", time.ctime(os.path.getctime(__file__)))
print("Size         :", os.path.getsize(__file__))

FILENAMES = [__file__, os.path.dirname(__file__), "/", "./broken_link"]

for file in FILENAMES:
    print("File        : {!r}".format(file))
    print("Absolute    :", os.path.isabs(file))
    print("Is File?    :", os.path.isfile(file))
    print("Is Dir?     :", os.path.isdir(file))
    print("Is Link?    :", os.path.islink(file))
    print("Mountpoint? :", os.path.ismount(file))
    print("Exists?     :", os.path.exists(file))
    print("Link Exists?:", os.path.lexists(file))
    print()
