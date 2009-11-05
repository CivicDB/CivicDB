#!/usr/bin/env python

import magic

import database

if __name__ == '__main__':
    converter_path = os.path.abspath('converters')

    converters = []
    if os.path.isdir(converter_path):
        # Get the names of files in the converters directory.
        files = os.listdir(converter_path)
        # Canonicalize the pathnames of files in the converters directory.
        files = [os.path.abspath(os.path.join(converter_path, file)) for file in files]
        # Converters must be executable
        files = [file for file in files if os.access(file, os.X_OK)]
#        # Converters express their input and output formats in the filename
#        files = [file for file in files if file.find('2') != -1]
        for file in files:
            converters.append(converter(path = file))

    for dataset in database.hopper():
        for converter in converters:
            if converter.accepts(object = dataset):
                print '     + file converter located: ' + converter.name()
                success = converter.process(object = dataset)
                if success:
                        print '     + file processed: ' + dataset.target()
                        break
                else:
                    print '     - file processing failed'
            else:
                print '     - file has no converter'
