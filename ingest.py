#!/usr/bin/env python

import hashlib
import os
import subprocess
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
        self._path = path
        self._md5 = hash(self._path)
    def filename(self):
        return self._path
    def hash(self):
        return self._md5

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
        self._path = path
        self._name = os.path.basename(self._path)
        [self._input, self._output] = self._name.split('2')
    def accepts(self, object):
        process = subprocess.Popen([self._path, '--test', object.filename()])
        process.wait()
        return process.returncode == 0
    def process(self, object):
        input_filename = object.filename()
        output_filename = os.path.splitext(input_filename)[0] + '.xml'
        process = subprocess.Popen([self._path, input_filename],
            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        process.wait()
        try:
            [out, err] = process.communicate()
            if err:
                print 'Errors occured while processing ' + input_filename
                print 'Error messages from ' + self._path + ':'
                print err
            if out:
                output_file = open(output_filename, 'w')
                output_file.write(out)
                output_file.close()
        except ValueError:
            # Pipes are empty
            pass
        return entry(path = output_filename)

if __name__ == '__main__':
    hopper_path = os.path.abspath('hopper')
    database_path = os.path.abspath('database')
    converter_path = os.path.abspath('converters')
    products_path = os.path.abspath('products')

    converters = []
    if os.path.isdir(converter_path):
        # Canonicalize the pathnames of files in the converters directory.
        files = [os.path.abspath(file) for file in os.listdir(converter_path)]
        # Converters must be executable
        files = [file for file in files if os.access(file, os.X_OK)]
        # Converters express their input and output formats in the filename
        files = [file for file in files if file.find('2') != -1]
        for file in files:
            converters.append(converter(path = file))

    if len(sys.argv[1:]) > 0:
        hopper_path = sys.argv[1]
    if os.path.isdir(hopper_path):
        watcher = watch(path = hopper_path)
        db = metadata(database_path)
        while True:
            filename = watcher.next()
            input_object = entry(path = filename)
            if not db.has_key(input_object.hash()):
                db[input_object.hash()] = input_object
                for converter in converters:
                    if converter.accepts(object = input_object):
                        output_object = converter.process(object = input_object)
                        break
    else:
        print hopper + ' does not appear to exist.'
