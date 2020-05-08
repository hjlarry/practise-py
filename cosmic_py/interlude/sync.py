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
