#!/usr/bin/env python

import hashlib
import os
import sys
import time

# Queries given directory at given refresh interval (expressed in seconds)
# If the file's modification time is different than the last time we saw
# it, or if this is the first time we have seen it, yield the filename.
def watch(path, refresh = 10.0):
    modtimes = dict()
    while True:
        cycle = time.time()
        if os.path.exists(path):
            present = os.listdir(path)
            present = [os.path.join(path, file) for file in present]
            missing = [key for key in modtimes.keys() if key not in present]
            for file in missing:
                del modtimes[file]
            for file in present:
                modtime = os.path.getmtime(file)
                if not modtimes.has_key(file) or modtimes[file] != modtime:
                    modtimes[file] = modtime
                    yield file
        else:
            modtimes.clear()
        remaining = time.time() - cycle
        if refresh > remaining:
            time.sleep(refresh - remaining)

def hash(path):
    if os.path.isfile(path):
        file = open(path)
        checksum = hashlib.md5()
        while True:
            data = file.read(2**20)
            if data:
                checksum.update(data)
            else:
                break
        file.close()
        return checksum.hexdigest()

class entry:
    def __init__(self, path):
        self.path = path
        self.md5 = hash(self.path)

class metadata(dict):
    def __init__(self, path):
        dict.__init__(self)
    def _read(self):
        # Syncronize the cached version in memory with the version on disk
        # if necessary.  We don't really know who else might be manipulating
        # the database at the same time, and in fact we can't really protect
        # ourselves from a truly bad actor, but by adhering to this simple
        # locking mechanism we can protect ourselves from conflicts with
        # other unknown programs which manipulate or reference the database.
        pass
    def _write(self):
        # Same as _read, but in the opposite direction.  Due to our locking
        # mechanism, we do not behave nicely if the dictionary has changed
        # while we hold the lock.  If you don't respect our lock we feel
        # no need to respect your changes.
        pass
    def _lock(self):
        pass
    def _unlock(self):
        pass
    def has_key(self, key):
        if self._lock():
            ret = dict.has_key(self, key)
            self._unlock()
            return ret
        else:
            return False
    def __getitem__(self, key):
        if self._lock():
            ret = dict.__getitem__(self, key)
            self._unlock()
            return ret
        else:
            return None
    def __setitem__(self, key, value):
        if self._lock():
            dict.__setitem__(self, key, value)
            self._unlock()
    def __delitem__(self, key):
        if self._lock():
            dict.__delitem__(self, key)
            self._unlock()
    def keys(self):
        print 'keys'
        return dict.keys(self)

class converter:
    def __init__(self, path):
        pass
    def process(self, path):
        pass

if __name__ == '__main__':
    hopper = os.path.abspath('hopper')
    database = os.path.abspath('database')
    converters = os.path.abspath('converters')
    products = os.path.abspath('products')

    if len(sys.argv[1:]) > 0:
        hopper = sys.argv[1]
    if os.path.isdir(hopper):
        watcher = watch(path = hopper)
        db = metadata(database)
        while True:
            filename = watcher.next()
            object = entry(path = filename)
            if not db.has_key(object.md5):
                db[object.md5] = entry
                (db[object.md5])
    else:
        print hopper + ' does not appear to exist.'
