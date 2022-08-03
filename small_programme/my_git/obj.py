import re
import os
import zlib
import sys
import collections
import hashlib

from ref import ref_create, ref_resolve

def object_read(repo, sha):
    """Read object object_id from Git repository repo.  Return a
    GitObject whose exact type depends on the object."""

    path = os.path.join(repo.git_obj_dir, sha[0:2], sha[2:])

    with open(path, "rb") as f:
        raw = zlib.decompress(f.read())

        # Read object type
        x = raw.find(b" ")
        fmt = raw[0:x]

        # Read and validate object size
        y = raw.find(b"\x00", x)
        size = int(raw[x:y].decode("ascii"))
        if size != len(raw) - y - 1:
            raise Exception(f"Malformed object {sha}: bad length")

        # Pick constructor
        if fmt == b"commit":
            c = GitCommit
        elif fmt == b"tree":
            c = GitTree
        elif fmt == b"tag":
            c = GitTag
        elif fmt == b"blob":
            c = GitBlob
        else:
            raise Exception(f"Unknown type {fmt.decode('ascii')} for object {sha}")

        obj = c(repo, raw[y + 1 :])
        obj.size = size
        # Call constructor and return object
        return obj


def object_find(repo, name, fmt=None, follow=True):
    sha = object_resolve(repo, name)

    if not sha:
        raise Exception(f"No such reference {name}.")

    if len(sha) > 1:
        raise Exception(
            "Ambiguous reference {0}: Candidates are:\n - {1}.".format(
                name, "\n - ".join(sha)
            )
        )

    sha = sha[0]

    if not fmt:
        return sha

    while True:
        obj = object_read(repo, sha)

        if obj.fmt == fmt:
            return sha

        if not follow:
            return None

        # Follow tags
        if obj.fmt == b"tag":
            sha = obj.kvlm[b"object"].decode("ascii")
        elif obj.fmt == b"commit" and fmt == b"tree":
            sha = obj.kvlm[b"tree"].decode("ascii")
        else:
            return None


def object_write(obj, actually_write=True):
    # Serialize object data
    data = obj.serialize()
    # Add header
    result = obj.fmt + b" " + str(len(data)).encode() + b"\x00" + data
    # Compute hash
    sha = hashlib.sha1(result).hexdigest()

    if actually_write:
        # Compute path
        dir_path = os.path.join(obj.repo.git_obj_dir, sha[0:2])
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        path = os.path.join(dir_path, sha[2:])
        with open(path, "wb") as f:
            # Compress and write
            f.write(zlib.compress(result))

    return sha


def object_resolve(repo, name):
    """
    Resolve name to an object hash in repo.

    This function is aware of:

    - the HEAD literal
    - short and long hashes
    """
    candidates = list()
    hashRE = re.compile(r"^[0-9A-Fa-f]{4,40}$")

    # Empty string?  Abort.
    if not name.strip():
        return None

    # Head is nonambiguous
    if name == "HEAD":
        return [ref_resolve(repo, "HEAD")]

    if hashRE.match(name):
        if len(name) == 40:
            # This is a complete hash
            return [name.lower()]

        # This is a small hash 4 seems to be the minimal length
        # for git to consider something a short hash.
        # This limit is documented in man git-rev-parse
        name = name.lower()
        prefix = name[0:2]
        path = os.path.join(repo.git_obj_dir, prefix)
        if path:
            rem = name[2:]
            for f in os.listdir(path):
                if f.startswith(rem):
                    candidates.append(prefix + f)
    return candidates


def object_hash(fd, fmt, repo=None):
    data = fd.read()

    # Choose constructor depending on
    # object type found in header.
    if fmt == b"commit":
        obj = GitCommit(repo, data)
    elif fmt == b"tree":
        obj = GitTree(repo, data)
    elif fmt == b"tag":
        obj = GitTag(repo, data)
    elif fmt == b"blob":
        obj = GitBlob(repo, data)
    else:
        raise Exception(f"Unknown type {fmt}!")

    return object_write(obj, repo)


def cat_file(repo, obj, fmt=None):
    obj = object_read(repo, object_find(repo, obj, fmt=fmt))
    print(obj)


class GitObject:

    repo = None
    fmt = None
    size = 0

    def __init__(self, repo, data=None):
        self.repo = repo

        if data != None:
            self.deserialize(data)

    def serialize(self):
        """
        This function MUST be implemented by subclasses.

        It must read the object's contents from self.data, a byte string, and do
        whatever it takes to convert it into a meaningful representation.  What exactly that means depend on each subclass.
        """
        raise Exception("Unimplemented!")

    def deserialize(self, data):
        raise Exception("Unimplemented!")

    def display(self):
        return self.serialize()

    def __str__(self):
        return f"type: {self.fmt.decode()}\r\nsize: {self.size}\r\ncontent:\r\n{self.display()}"


class GitBlob(GitObject):
    fmt = b"blob"

    def serialize(self):
        return self.blobdata

    def deserialize(self, data):
        self.blobdata = data


class GitCommit(GitObject):
    fmt = b"commit"

    def serialize(self):
        ret = b""

        # Output fields
        for k in self.kvlm.keys():
            # Skip the message itself
            if k == b"":
                continue
            val = self.kvlm[k]
            # Normalize to a list
            if type(val) != list:
                val = [val]

            for v in val:
                ret += k + b" " + (v.replace(b"\n", b"\n ")) + b"\n"

        # Append message
        ret += b"\n" + self.kvlm[b""]

        return ret

    def deserialize(self, data, start=0, dct=None):
        self.kvlm = self.kvlm_parse(data)

    def kvlm_parse(self, raw, start=0, dct=None):
        """can parse the commit object and tag object"""
        if not dct:
            dct = collections.OrderedDict()

        # We search for the next space and the next newline.
        spc = raw.find(b" ", start)
        nl = raw.find(b"\n", start)

        # If space appears before newline, we have a keyword.

        # Base case
        # =========
        # If newline appears first (or there's no space at all, in which
        # case find returns -1), we assume a blank line.  A blank line
        # means the remainder of the data is the message.
        if (spc < 0) or (nl < spc):
            assert nl == start
            dct[b""] = raw[start + 1 :]
            return dct

        # Recursive case
        # ==============
        # we read a key-value pair and recurse for the next.
        key = raw[start:spc]

        # Find the end of the value.  Continuation lines begin with a
        # space, so we loop until we find a "\n" not followed by a space.
        end = start
        while True:
            end = raw.find(b"\n", end + 1)
            if raw[end + 1] != ord(" "):
                break

        # Grab the value
        # Also, drop the leading space on continuation lines
        value = raw[spc + 1 : end].replace(b"\n ", b"\n")

        # Don't overwrite existing data contents
        if key in dct:
            if type(dct[key]) == list:
                dct[key].append(value)
            else:
                dct[key] = [dct[key], value]
        else:
            dct[key] = value

        return self.kvlm_parse(raw, start=end + 1, dct=dct)

    def display(self):
        return self.serialize().decode()


class GitTreeLeaf:
    def __init__(self, mode, path, sha):
        self.mode = mode
        self.path = path
        self.sha = sha


class GitTree(GitObject):
    fmt = b"tree"

    def serialize(self):
        # @FIXME Add serializer!
        ret = b""
        for i in self.items:
            ret += i.mode
            ret += b" "
            ret += i.path
            ret += b"\x00"
            sha = int(i.sha, 16)
            # @FIXME Does
            ret += sha.to_bytes(20, byteorder="big")
        return ret

    def tree_parse_one(self, raw, start=0):
        # Find the space terminator of the mode
        x = raw.find(b" ", start)
        assert x - start == 5 or x - start == 6

        # Read the mode
        mode = raw[start:x]

        # Find the NULL terminator of the path
        y = raw.find(b"\x00", x)
        # and read the path
        path = raw[x + 1 : y]

        # Read the SHA and convert to an hex string
        sha = hex(int.from_bytes(raw[y + 1 : y + 21], "big"))[
            2:
        ]  # hex() adds 0x in front,
        # we don't want that.
        return y + 21, GitTreeLeaf(mode, path, sha)

    def deserialize(self, data):
        pos = 0
        max = len(data)
        self.items = list()
        while pos < max:
            pos, leaf = self.tree_parse_one(data, pos)
            self.items.append(leaf)

    def display(self):
        rs = []
        for item in self.items:
            s = "{0} {1} {2}\t{3}".format(
                "0" * (6 - len(item.mode)) + item.mode.decode("ascii"),
                # Git's ls-tree displays the type
                # of the object pointed to.  We can do that too :)
                object_read(self.repo, item.sha).fmt.decode("ascii"),
                item.sha,
                item.path.decode("ascii"),
            )
            rs.append(s)
        return "\r\n".join(rs)


class GitTag(GitCommit):
    fmt = b"tag"


def tag_create(repo, name, reference, create_tag_object):
    # get the GitObject from the object reference
    sha = object_find(repo, reference)

    if create_tag_object:
        # create tag object (commit)
        tag = GitTag(repo)
        tag.kvlm = collections.OrderedDict()
        tag.kvlm[b"object"] = sha.encode()
        tag.kvlm[b"type"] = b"commit"
        tag.kvlm[b"tag"] = name.encode()
        tag.kvlm[b"tagger"] = b"The soul eater <grim@reaper.net>"
        tag.kvlm[
            b""
        ] = b"This is the commit message that should have come from the user\n"
        tag_sha = object_write(tag, repo)
        # create reference
        ref_create(repo, "tags/" + name, tag_sha)
    else:
        # create lightweight tag (ref)
        ref_create(repo, "tags/" + name, sha)


def log_graphviz(repo, sha, seen):

    if sha in seen:
        return
    seen.add(sha)

    commit = object_read(repo, sha)
    assert commit.fmt == b"commit"

    if not b"parent" in commit.kvlm.keys():
        # Base case: the initial commit.
        return

    parents = commit.kvlm[b"parent"]

    if type(parents) != list:
        parents = [parents]

    for p in parents:
        p = p.decode("ascii")
        print(f"c_{sha} -> c_{p};")
        log_graphviz(repo, p, seen)
