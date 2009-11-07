#!/usr/bin/env python

import collections
import hashlib
import os
import time

class indexer:
    def __init__(self, path):
        self._path = path
        if os.path.exists(self._path):
            if os.path.isdir(self._path):
                files = os.listdir(self._path)
                self._present = collections.deque(\
                    [os.path.join(self._path, file) for file in files])
            else:
                self._present = collections.deque([self._path])
    def __iter__(self):
        return self
    def next(self):
        if len(self._present) > 0:
            return entry(unprocessed = self._present.popleft())
        else:
            return None

# Queries given directory at given refresh interval (expressed in seconds)
# If the file's modification time is different than the last time we saw
# it, or if this is the first time we have seen it, yield the filename.
def watch(path, refresh = 10.0):
    modtimes = dict()
    print ' + monitoring: ' + path
    while True:
        cycle = time.time()
        if os.path.exists(path):
            present = os.listdir(path)
            present = [os.path.join(path, file) for file in present]
            missing = [key for key in modtimes.keys() if key not in present]
            for file in missing:
                print '   - file missing: ' + file
                del modtimes[file]
            for file in present:
                modtime = os.path.getmtime(file)
                if not modtimes.has_key(file) or modtimes[file] != modtime:
                    modtimes[file] = modtime
                    print '   + file noticed: ' + file
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
    def __init__(self, unprocessed):
        self._unprocessed = unprocessed
        self._processed = os.path.join(os.path.abspath('products'), 
            os.path.splitext(os.path.basename(self._unprocessed))[0] + '.xml')
        self._md5 = hash(self._unprocessed)
    def __enter__(self):
        pass
    def __exit__(self, type, value, traceback):
        pass
    def filename(self):
        return self._unprocessed
    def target(self):
        return self._processed
    def hash(self):
        return self._md5

class metadata(dict):
    def __init__(self):
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
#    def keys(self):
#        print 'keys'
#        return dict.keys(self)

def hopper():
    watcher = watch(path = os.path.abspath('hopper'))
    hashes = metadata()
    while True:
        file = watcher.next()
        dataset = entry(unprocessed = file)
        if not dataset.hash() in hashes:
            print '     + file hash calculated: ' + str(dataset.hash())
            hashes[dataset.hash()] = dataset
            yield dataset
        else:
            print '     - file already processed'
