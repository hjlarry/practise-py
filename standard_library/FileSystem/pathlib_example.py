import pathlib
import itertools
import os
import time
import stat

print("一、 路径构建")
usr_local = pathlib.Path("/usr/local")
share = usr_local / ".." / "share"
print("relative:", share)
# 生成绝对路径
print("resolve():", share.resolve())
# 通过列表构建
root = pathlib.PurePosixPath("/")
subdirs = ["usr", "local", "tt"]
usr_local = root.joinpath(*subdirs)
print("joinpath():", usr_local)
print()
ind = pathlib.PurePosixPath("source/pathlib/index.rst")
print(ind)
# 通过已有path和名称构建
py = ind.with_name("pathlib_from_existing.py")
print("with_name():", py)
# 通过已有path和后缀构建
pyc = ind.with_suffix(".pyc")
print("with_suffix():", pyc)
print()

print("二、 路径解析")
p = pathlib.Path("/usr/local/sth/demo.py")
print("parts:", p.parts)
print("parent:", p.parent)
print("parents:", list(p.parents))
print("name:", p.name)
print("suffix:", p.suffix)
print("stem:", p.stem)
home = pathlib.Path.home()
print("home:", home)
cwd = pathlib.Path.cwd()
print("cwd:", cwd)
print()

print("三、 迭代目录")
p = pathlib.Path(".")
print("输出所有文件:")
for f in p.iterdir():
    print(f, end="|")
print()
print("输出所有.py文件:")
for f in p.glob("*.py"):
    print(f, end="|")
# rglob(*.py) == glob(**/*.py) 递归查找
print()
print("递归查找并输出所有p开头的.ipynb文件:")
for f in p.rglob("p*.ipynb"):
    print(f, end="|")
print()
print()

print("四、 操作文件、目录、链接")
f = pathlib.Path("test_files/example.txt")
f.write_bytes(b"hello world")
with f.open("r") as handle:
    print(f"通过open()读取: {handle.read()!r}")
print(f"通过read_text()读取: {f.read_text()!r}")

print("链接一个文件:")
p = pathlib.Path("test_files/example_dir")
if p.exists():
    # 只能移除空目录,目录不存在或其中有文件会抛异常
    p.rmdir()
p.mkdir()
p = pathlib.Path("test_files/example_link")
if not p.exists():
    # 使用 symlink_to() 创建一个符号链接
    p.symlink_to("sth.txt")
print(p)
# 然后用 resolve() 方法读取符号链接指向的目标的名称
print(p.resolve())
print(p.resolve().name)

root = pathlib.Path("test_files/test")
if root.exists():
    for f in root.iterdir():
        f.unlink()
else:
    root.mkdir()
# 创建测试文件
(root / "file").write_text("hello, this is a test file")
(root / "symlink").symlink_to("file")
# fifo是命名管道文件
os.mkfifo(str(root / "fifo"))

to_scan = itertools.chain(
    root.iterdir(), [pathlib.Path("/dev/disk0"), pathlib.Path("/dev/console")]
)
print("文件类别信息:")
print(
    f"{'Name':25s} {'IsFile':^5} {'IsDir':^5} {'IsLink':>5} {'IsFIFO':>5} {'IsBlock':>5} {'IsCharacter':^5}"
)
for f in to_scan:
    print(
        f"{str(f):25s} {f.is_file():^5} {f.is_dir():^5} {f.is_symlink():^5} {f.is_fifo():^5} {f.is_block_device():^5} {f.is_char_device():^5}"
    )

print("某文件基础信息:")
p = pathlib.Path("test_files/example.txt")
stat_info = p.stat()
print(p, " statinfo:")
print(f" Size:{stat_info.st_size}")
print(f" Permessions:{oct(stat_info.st_mode)}")
print(f" Owner:{stat_info.st_uid}")
print(f" Owner:{p.owner()}")
print(f" Group:{p.group()}")
print(f" Device:{stat_info.st_dev}")
print(f" Created:{time.ctime(stat_info.st_ctime)}")
print(f" Last Modified:{time.ctime(stat_info.st_mtime)}")
print(f" Last Accessed:{time.ctime(stat_info.st_atime)}")

print("测试touch前后文件更新时间变化:")
p = pathlib.Path("test_files/touch")
if p.exists():
    print("already have this file")
else:
    print("creat a file")
p.touch()
start = p.stat()
time.sleep(1)
p.touch()  # 多次运行touch更新文件的时间
end = p.stat()
print("Start:", time.ctime(start.st_mtime))
print("End  :", time.ctime(end.st_mtime))

# 创建一个全新的测试文件
print("测试某文件权限:")
f = pathlib.Path("test_files/pathlib_chmod_example.txt")
if f.exists():
    f.unlink()
f.write_text("contents")

# 使用 stat 方法来检测文件权限
existing_permissions = stat.S_IMODE(f.stat().st_mode)
print("Before: {:o}".format(existing_permissions))

# 决定用啥方法来处理
if not (existing_permissions & os.X_OK):
    print("Adding execute permission")
    new_permissions = existing_permissions | stat.S_IXUSR
else:
    print("Removing execute permission")
    # 使用 xor 来移除用户可执行权限
    new_permissions = existing_permissions ^ stat.S_IXUSR

# 修改权限，并打印修改后的权限结果
f.chmod(new_permissions)
after_permissions = stat.S_IMODE(f.stat().st_mode)
print("After: {:o}".format(after_permissions))
