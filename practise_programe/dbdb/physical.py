import partalocker


class Storage:
    def __init__(self, f):
        self._f = f

    def lock(self):
        if not self.locked:
            partalocker.lock(self._f, partalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def commit_root_address(self, root_address):
        self.lock()
        self._f.flush()
        self._seek_superblock()
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()
