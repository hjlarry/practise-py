from pathlib import Path


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
