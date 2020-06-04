import configparser
import os

class GitRepository:
    """A git repository"""

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        self.git_obj_dir =  os.path.join(self.gitdir, "objects")
        self.git_ref_dir =  os.path.join(self.gitdir, "refs")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git repository {path}")

        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = os.path.join(self.gitdir, "config")

        if os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(f"Unsupported repositoryformatversion {vers}")

    def create(self):
        """
        Create a new repository at path.
        .git is the git directory itself, which contains:
            .git/objects/  the object store.
            .git/refs/ the reference store. It contains two subdirectories, heads and tags.
            .git/HEAD, a reference to the current HEAD.
            .git/config, the repository’s configuration file.
            .git/description, the repository’s description file.
        """

        # First, we make sure the path either doesn't exist or is an empty dir.
        if os.path.exists(self.worktree):
            if not os.path.isdir(self.worktree):
                raise Exception(f"{path} is not a directory!")
            if os.listdir(self.worktree):
                raise Exception(f"{path} is not empty!")
        else:
            os.makedirs(self.worktree)

        os.makedirs(os.path.join(self.gitdir, "branches"))
        os.makedirs(self.git_obj_dir)
        os.makedirs(os.path.join(self.git_ref_dir, "tags"))
        os.makedirs(os.path.join(self.git_ref_dir, "heads"))

        # .git/description
        with open(os.path.join(self.gitdir, "description"), "w") as f:
            f.write(
                "Unnamed repository; edit this file 'description' to name the repository.\n"
            )

        # .git/HEAD
        with open(os.path.join(self.gitdir, "HEAD"), "w") as f:
            f.write("ref: refs/heads/master\n")

        with open(os.path.join(self.gitdir, "config"), "w") as f:
            config = self.default_config()
            config.write(f)


    def default_config(self):
        ret = configparser.ConfigParser()

        ret.add_section("core")
        ret.set("core", "repositoryformatversion", "0")
        ret.set("core", "filemode", "false")
        ret.set("core", "bare", "false")

        return ret


def repo_find(path=".", required=True):
    path = os.path.realpath(path)

    if os.path.isdir(os.path.join(path, ".git")):
        return GitRepository(path)

    # If we haven't returned, recurse in parent, if w
    parent = os.path.realpath(os.path.join(path, ".."))

    if parent == path:
        # Bottom case
        # os.path.join("/", "..") == "/":
        # If parent==path, then path is root.
        if required:
            raise Exception("No git directory.")
        else:
            return None

    # Recursive case
    return repo_find(parent, required)