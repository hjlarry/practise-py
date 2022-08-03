import collections
import os


def ref_resolve(repo, ref):
    p = os.path.join(repo.gitdir, ref)
    with open(p, "r") as fp:
        data = fp.read()[:-1]
        # Drop final \n ^^^^^
    if data.startswith("ref: "):
        return ref_resolve(repo, data[5:])
    else:
        return data


def ref_list(repo, path=None):
    if not path:
        path = repo.git_ref_dir
    ret = collections.OrderedDict()
    # Git shows refs sorted.  To do the same, we use
    # an OrderedDict and sort the output of listdir
    for f in sorted(os.listdir(path)):
        can = os.path.join(path, f)
        if os.path.isdir(can):
            ret[f] = ref_list(repo, can)
        else:
            ret[f] = ref_resolve(repo, can)

    return ret


def show_ref(repo, refs, with_hash=True, prefix=""):
    for k, v in refs.items():
        if type(v) == str:
            print(
                "{0}{1}{2}".format(
                    v + " " if with_hash else "", prefix + "/" if prefix else "", k
                )
            )
        else:
            show_ref(
                repo,
                v,
                with_hash=with_hash,
                prefix="{0}{1}{2}".format(prefix, "/" if prefix else "", k),
            )


def ref_create(repo, ref_name, sha):
    with open(os.path.join(repo.git_ref_dir, ref_name), "w") as fp:
        fp.write(sha + "\n")
