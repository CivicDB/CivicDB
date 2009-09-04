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
                modtime = os.stat(file).st_mtime
                if not modtimes.has_key(file) or modtimes[file] != modtime:
                    modtimes[file] = modtime
                    yield file
        else:
            modtimes.clear()
        remaining = time.time() - cycle
        if refresh > remaining:
            time.sleep(refresh - remaining)

def hash(path):
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
    def __contains__(self, item):
        print 'contains'
        return dict.__contains__(self, item)
    def __getitem__(self, key):
        print 'get'
        return dict.__getitem__(self, key)
    def __setitem__(self, key, value):
        print 'set'
        return dict.__setitem__(self, key, value)
    def __delitem__(self, key):
        print 'del'
        return dict.__delitem__(self, key)
    def keys(self):
        print 'keys'
        return dict.keys(self)

if __name__ == '__main__':
    hopper = os.path.join(os.getcwd(), 'hopper')
    database = os.path.join(os.getcwd(), 'database')
    products = os.path.join(os.getcwd(), 'products')

    if len(sys.argv[1:]) > 0:
        hopper = sys.argv[1]
    if os.path.exists(hopper):
        watcher = watch(path = hopper)
        db = metadata(database)
        while True:
            filename = watcher.next()
            print 'we found ' + filename
            object = entry(path = filename)
            if db.has_key(object.md5):
                print 'file ' + object.path + ' is already stored in metadata'
                print 'the checksum is ' + object.md5
            else:
                db[object.md5] = entry
    else:
        print hopper + ' does not appear to exist.'
