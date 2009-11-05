#!/usr/bin/env python

import os
import subprocess

class converter:
    def __init__(self, path):
        self._path = path
        self._name = os.path.basename(self._path)
        [self._input_format, self._output_format] = self._name.split('2')
    def name(self):
        return self._name
    def accepts(self, object):
        process = subprocess.Popen([self._path, '--test', object.filename()])
        while process.poll() == None:
            # Don't care about output, just the return code.
            try:
                process.communicate()
            except ValueError:
                break
        return process.returncode == 0
    def process(self, object):
        input_filename = object.filename()
        output_filename = object.target()
        print '     + conversion input: ' + input_filename
        process = subprocess.Popen([self._path, input_filename],
            stdout = subprocess.PIPE)#, stderr = subprocess.PIPE)
        output_file = open(output_filename, 'w')
        while process.returncode == None:
            try:
                [out, err] = process.communicate()
                if out:
                    output_file.write(out)
            except ValueError:
                # Pipes are empty.
                break
#        # Slurp any final data
#        try:
#            [out, err] = process.communicate()
#            output_file.write(out)
#        except ValueError:
#            # Pipes are empty.  Not surprising.
#            pass
        output_file.close()
        # Decide success or failure.
        if process.returncode == 0:
            print '     + conversion result: ' + output_filename
            return True
        else:
            print '     - converter failed'
            return False

def list(path = None):
    if not path:
        path = os.path.abspath()

    converters = []
    if os.path.isdir(path):
        # Get the names of files in the converters directory.
        files = os.listdir(path)
        # Canonicalize the pathnames of files in the converters directory.
        files = [os.path.abspath(os.path.join(path, file)) for file in files]
        # Converters must be executable
        files = [file for file in files if os.access(file, os.X_OK)]
#        # Converters express their input and output formats in the filename
#        files = [file for file in files if file.find('2') != -1]
        for file in files:
            converters.append(converter(path = file))
    return converters

if __name__ == '__main__':
    path = os.path.abspath('.')
    print 'Known converters in ' + path + ':'
    print list(path = path)
