import partalocker


class Storage:
    def lock(self):
        if not self.locked:
            partalocker.lock(self._f, partalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False
