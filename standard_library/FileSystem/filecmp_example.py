import os
import filecmp
import pprint


def mkfile(filename, body=None):
    with open(filename, "w") as f:
        f.write(body)
    return


def make_example_dir(top):
    if not os.path.exists(top):
        os.mkdir(top)
    curdir = os.getcwd()
    os.chdir(top)

    os.mkdir("dir1")
    os.mkdir("dir2")

    mkfile("dir1/file_only_in_dir1", body="file_only_in_dir1")
    mkfile("dir2/file_only_in_dir2", body="file_only_in_dir2")

    os.mkdir("dir1/dir_only_in_dir1")
    os.mkdir("dir2/dir_only_in_dir2")

    os.mkdir("dir1/common_dir")
    os.mkdir("dir2/common_dir")

    mkfile("dir1/common_file", "this file is the same")
    mkfile("dir2/common_file", "this file is the same")

    mkfile("dir1/not_the_same", "this file is dir1")
    mkfile("dir2/not_the_same", "this file is dir2")

    mkfile("dir1/file_in_dir1", "This is a file in dir1")
    os.mkdir("dir2/file_in_dir1")

    os.chdir(curdir)
    return


# 创建测试文件
make_example_dir("test_files")
make_example_dir("test_files/dir1/common_dir")
make_example_dir("test_files/dir2/common_dir")


print("一、 单个文件比较")
# shallow默认为True，即只比较os.stat()获取到的文件元信息，因此同时创建且大小相同的文件被认为是相同的，即使它们的内容不同
# shallow为False则比较文件内容
print(filecmp.cmp("test_files/dir1/common_file", "test_files/dir2/common_file"))
print(
    filecmp.cmp(
        "test_files/dir1/common_file", "test_files/dir2/common_file", shallow=False
    )
)
print(filecmp.cmp("test_files/dir1/not_the_same", "test_files/dir2/not_the_same"))
print(
    filecmp.cmp(
        "test_files/dir1/not_the_same", "test_files/dir2/not_the_same", shallow=False
    )
)
print()


print("二、 批量文件比较")
d1_contents = set(os.listdir("test_files/dir1"))
d2_contents = set(os.listdir("test_files/dir2"))
common = list(d1_contents & d2_contents)
# 先要构建公共文件夹
common_files = [f for f in common if os.path.isfile(os.path.join("test_files/dir1", f))]
print("Common files:", common_files)
match, mismatch, errors = filecmp.cmpfiles(
    "test_files/dir1", "test_files/dir2", common_files
)
print("Match:", match)
print("Mismatch:", mismatch)
print("Errors:", errors)
print()


print("三、 目录比较")
dc = filecmp.dircmp("test_files/dir1", "test_files/dir2", ignore=["common_file"])
print("LEFT:")
pprint.pprint(dc.left_list)
print("RIGHT:")
pprint.pprint(dc.right_list)

print("COMMON:")
pprint.pprint(dc.common)
print("LEFT only:")
pprint.pprint(dc.left_only)
print("RIGHT only:")
pprint.pprint(dc.right_only)
print("COMMON dir:")
pprint.pprint(dc.common_dirs)
print("COMMON files:")
pprint.pprint(dc.common_files)
print("COMMON funny:")
pprint.pprint(dc.common_funny)  # 在一个目录中是一个文件，另一个中是子目录

print("Same  :", dc.same_files)
print("Diff  :", dc.diff_files)
print("Funny :", dc.funny_files)
print("Subdir :", dc.subdirs)
