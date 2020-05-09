# 目标：同步两个文件夹，目标文件夹没有的文件则复制过去，多出的文件则删除，只文件名称不同的文件则改名
# 第一个版本，具体的业务和I/O代码紧密耦合，必须要调用hashlib、os、shutil等这些库，造成代码的可扩展性不强。
# 例如需要加一个--dry-run标签只输出代码将要做什么而并非真的要做时、或者需要同步远程服务器时，都变得不易扩展
# sync_v2.py增加了一层抽象去解决这个问题，也更易于测试

import hashlib
import os
import shutil
import pathlib

BLOCKSIZE = 65536


def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as f:
        buf = f.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()


def sync(source, dest):
    source_hashed = {}
    for folder, _, files in os.walk(source):
        for fn in files:
            f = pathlib.Path(folder) / fn
            source_hashed[hash_file(f)] = fn

    seen = set()

    for folder, _, files in os.walk(dest):
        for fn in files:
            dest_path = pathlib.Path(folder) / fn
            dest_hash = hash_file(dest_path)
            seen.add(dest_hash)

            if dest_hash not in source_hashed:
                dest_path.remove()
            elif dest_hash in source_hashed and fn != source_hashed[dest_hash]:
                shutil.move(dest_path, pathlib.Path(folder) / source_hashed[dest_hash])

    for src_hash, fn in source_hashed.items():
        if src_hash not in seen:
            shutil.copy(pathlib.Path(source) / fn, pathlib.Path(dest) / fn)
