#!/usr/bin/env python

from __future__ import with_statement
import os
import subprocess
import sys
import time

import converters
import database

if __name__ == '__main__':
    converter_path = os.path.abspath('converters')
    products_path = os.path.abspath('products')

    converters = converters.list(path = converter_path)

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
