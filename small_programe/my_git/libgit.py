import argparse
import sys

from repo import GitRepository, repo_find
from obj import (
    cat_file,
    object_hash,
    object_find,
    log_graphviz,
    object_read,
    tag_create,
)
from ref import ref_list, show_ref

argparser = argparse.ArgumentParser(description="The stupid content tracker")

argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command == "add":
        cmd_add(args)
    elif args.command == "cat-file":
        cmd_cat_file(args)
    elif args.command == "checkout":
        cmd_checkout(args)
    elif args.command == "commit":
        cmd_commit(args)
    elif args.command == "hash-object":
        cmd_hash_object(args)
    elif args.command == "init":
        cmd_init(args)
    elif args.command == "log":
        cmd_log(args)
    elif args.command == "ls-tree":
        cmd_ls_tree(args)
    elif args.command == "merge":
        cmd_merge(args)
    elif args.command == "rebase":
        cmd_rebase(args)
    elif args.command == "rev-parse":
        cmd_rev_parse(args)
    elif args.command == "rm":
        cmd_rm(args)
    elif args.command == "show-ref":
        cmd_show_ref(args)
    elif args.command == "tag":
        cmd_tag(args)


def cmd_add(args):
    pass


def cmd_checkout(args):
    pass


def cmd_commit(args):
    pass


def cmd_merge(args):
    pass


def cmd_rebase(args):
    pass


def cmd_rm(args):
    pass


def cmd_show_ref(args):
    pass


argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")

argsp.add_argument(
    "path",
    metavar="directory",
    nargs="?",
    default=".",
    help="Where to create the repository.",
)


def cmd_init(args):
    repo = GitRepository(args.path, force=True)
    repo.create()


argsp = argsubparsers.add_parser(
    "cat-file", help="Provide content of repository objects"
)

argsp.add_argument("object", metavar="object", help="The object to display")


def cmd_cat_file(args):
    repo = repo_find()
    cat_file(repo, args.object)


argsp = argsubparsers.add_parser(
    "hash-object", help="Compute object ID and optionally creates a blob from a file"
)

argsp.add_argument(
    "-t",
    metavar="type",
    dest="type",
    choices=["blob", "commit", "tag", "tree"],
    default="blob",
    help="Specify the type",
)

argsp.add_argument(
    "-w",
    dest="write",
    action="store_true",
    help="Actually write the object into the database",
)

argsp.add_argument("path", help="Read object from <file>")


def cmd_hash_object(args):
    if args.write:
        repo = GitRepository(".")
    else:
        repo = None

    with open(args.path, "rb") as fd:
        sha = object_hash(fd, args.type.encode(), repo)
        print(sha)


argsp = argsubparsers.add_parser("log", help="Display history of a given commit.")
argsp.add_argument("commit", default="HEAD", nargs="?", help="Commit to start at.")


def cmd_log(args):
    repo = repo_find()

    print("digraph mylog{")
    log_graphviz(repo, object_find(repo, args.commit), set())
    print("}")


argsp = argsubparsers.add_parser("ls-tree", help="Pretty-print a tree object.")
argsp.add_argument("object", help="The object to show.")


def cmd_ls_tree(args):
    repo = repo_find()
    obj = object_read(repo, object_find(repo, args.object, fmt=b"tree"))

    for item in obj.items:
        print(
            "{0} {1} {2}\t{3}".format(
                "0" * (6 - len(item.mode)) + item.mode.decode("ascii"),
                # Git's ls-tree displays the type
                # of the object pointed to.  We can do that too :)
                object_read(repo, item.sha).fmt.decode("ascii"),
                item.sha,
                item.path.decode("ascii"),
            )
        )


argsp = argsubparsers.add_parser("show-ref", help="List references.")


def cmd_show_ref(args):
    repo = repo_find()
    refs = ref_list(repo)
    show_ref(repo, refs, prefix="refs")


argsp = argsubparsers.add_parser("tag", help="List and create tags")

argsp.add_argument(
    "-a",
    action="store_true",
    dest="create_tag_object",
    help="Whether to create a tag object",
)

argsp.add_argument("name", nargs="?", help="The new tag's name")

argsp.add_argument(
    "object", default="HEAD", nargs="?", help="The object the new tag will point to"
)


def cmd_tag(args):
    repo = repo_find()

    if args.create_tag_object:
        tag_create(
            repo, args.name, args.object, create_tag_object=True,
        )
    elif args.name:
        tag_create(repo, args.name, args.object, create_tag_object=False)
    else:
        refs = ref_list(repo)
        show_ref(repo, refs["tags"], with_hash=False)


argsp = argsubparsers.add_parser(
    "rev-parse", help="Parse revision (or other objects )identifiers"
)

argsp.add_argument(
    "--wyag-type",
    metavar="type",
    dest="type",
    choices=["blob", "commit", "tag", "tree"],
    default=None,
    help="Specify the expected type",
)

argsp.add_argument("name", help="The name to parse")


def cmd_rev_parse(args):
    if args.type:
        fmt = args.type.encode()

    repo = repo_find()

    print(object_find(repo, args.name, args.type, follow=True))

