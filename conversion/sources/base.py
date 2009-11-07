#!/usr/bin/env python

import collections
import hashlib
import os
import threading

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

class indexer:
    def __init__(self, path):
        self._path = path
        self._new = self._index()
    def __iter__(self):
        return self
    def _index(self):
        return collections.deque()
    def _wrap(self, path):
        return entry(unprocessed = path)
    def next(self):
        if len(self._new) > 0:
            return self._wrap(path = self._new.popleft())
        else:
            return None

class watcher(indexer):
    def __init__(self, path):
        self._old = collections.deque()
        self._interval = 10.0
        self._thread = threading.Timer(self._interval, self._reindex)
        indexer.__init__(self, path = path)
    def __del__(self):
        if self._thread:
            self._thread.cancel()
    def _lock(self):
        pass
    def _unlock(self):
        pass
    def _reindex(self):
        self._thread = None
        found = self._index()
        self._lock()
        seen = set(self._old + self._new)
        for path in found:
            if path not in seen:
                self._new.append(path)
        self._unlock()
        self._thread = threading.Timer(self._interval, self._reindex)
