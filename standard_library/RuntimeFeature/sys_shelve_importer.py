import imp
import os
import shelve
import sys


def _mk_init_name(fullname):
    if fullname.endswith(".__init__"):
        return fullname
    return fullname + ".__init__"


def _get_key_name(fullname, db):
    if fullname in db:
        return fullname
    init_name = _mk_init_name(fullname)
    if init_name in db:
        return init_name
    return None


class ShelveFinder:
    _maybe_recursing = False

    def __init__(self, path_entry):
        if ShelveFinder._maybe_recursing:
            raise ImportError
        try:
            # test the path_entry to see if it is a valid shelf
            try:
                ShelveFinder._maybe_recursing = True
                with shelve.open(path_entry, "r"):
                    pass
            finally:
                ShelveFinder._maybe_recursing = False
        except Exception as e:
            print(f"shelf could not import from {path_entry}: {e}")
            raise
        else:
            print(f"shelf add to import path: {path_entry}")
            self.path_entry = path_entry
        return

    def __str__(self):
        return f"<{self.__class__.__name__} for {self.path_entry!r}>"

    def find_module(self, fullname, path=None):
        path = path or self.path_entry
        print(f"looking for {fullname!r} in {path}")
        with shelve.open(self.path_entry, "r") as db:
            key_name = _get_key_name(fullname, db)
            if key_name:
                print(f"found it as {key_name}")
                return ShelveLoader(self.path_entry)
        print("not found")
        return None


class ShelveLoader:
    def __init__(self, path_entry):
        self.path_entry = path_entry

    def _get_filename(self, fullname):
        # Make up a fake filename that starts with the path entry, so pkgutil.get_data() works correctly.
        return os.path.join(self.path_entry, fullname)

    def get_source(self, fullname):
        print(f"loading source for {fullname} from shelf")
        try:
            with shelve.open(self.path_entry, "r") as db:
                key_name = _get_key_name(fullname, db)
                if key_name:
                    return db[key_name]
                raise ImportError(f"can not find source for {fullname}")
        except Exception as e:
            print("could not load source for ", fullname)
            raise ImportError(e)

    def get_code(self, fullname):
        source = self.get_source(fullname)
        print(f"compile code for {fullname}")
        return compile(source, self._get_filename(fullname), "exec", dont_inherit=True)

    def get_data(self, path):
        print(f"looking for data in {self.path_entry} for {path}")
        if not path.startswith(self.path_entry):
            raise IOError
        path = path[len(self.path_entry) + 1 :]
        key_name = "data:" + path
        try:
            with shelve.open(self.path_entry, "r") as db:
                return db[key_name]
        except Exception:
            raise IOError()

    def is_package(self, fullname):
        init_name = _mk_init_name(fullname)
        with shelve.open(self.path_entry, "r") as db:
            return init_name in db

    def load_module(self, fullname):
        source = self.get_source(fullname)
        if fullname in sys.modules:
            print(f"reusing module from import of {fullname}")
            mod = sys.modules[fullname]
        else:
            print(f"create a new module obj for {fullname}")
            mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        mod.__file__ = self._get_filename(fullname)
        mod.__name__ = fullname
        mod.__path__ = self.path_entry
        mod.__loader__ = self
        # PEP-366 specifies that package's set __package__ to
        # their name, and modules have it set to their parent
        # package (if any).
        if self.is_package(fullname):
            mod.__package__ = fullname
        else:
            mod.__package__ = ".".join(fullname.split(".")[:-1])
        if self.is_package(fullname):
            print("adding path to package")
            # Set __path__ for packages so we can find the sub-modules.
            mod.__path__ = [self.path_entry]
        else:
            print("import as regular module")

        print("execing source...")
        exec(source, mod.__dict__)
        print("done")
        return mod


import pkgutil
