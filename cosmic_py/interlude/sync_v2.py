import os
import hashlib
import shutil
from pathlib import Path

BLOCKSIZE = 65536


def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as f:
        buf = f.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()


def determine_actions(src_hashes, dst_hashes, src_folder, dst_folder):
    for sha, filename in src_hashes.items():
        if sha not in dst_hashes:
            sourcepath = Path(src_folder) / filename
            destpath = Path(dst_folder) / filename
            yield "copy", sourcepath, destpath
        elif dst_hashes[sha] != filename:
            oldpath = Path(dst_folder) / dst_hashes[sha]
            newpath = Path(dst_folder) / filename
            yield "move", oldpath, newpath

    for sha, filename in dst_hashes.items():
        if sha not in src_hashes:
            yield "delete", dst_folder / filename


def read_paths_and_hashes(root):
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes


def sync(source, dest):
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = read_paths_and_hashes(dest)
    actions = determine_actions(source_hashes, dest_hashes, source, dest)
    for action, *paths in actions:
        if action == "copy":
            shutil.copyfile(*paths)
        if action == "move":
            shutil.move(*paths)
        if action == "delete":
            os.remove(paths[0])
