#!/usr/bin/env python

from __future__ import with_statement
import optparse
import os
import subprocess
import sys
import time

import converters
import database
import sources.web
import sources.file

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_options("-d", "--dir", dest = "dirs", \
        help = "Convert all files in DIR", metavar = "DIR", action = "append")
    parser.add_option("-f", "--file", dest = "files", \
        help = "Convert FILE", metavar = "FILE", action = "append")
    parser.add_option("--api", dest = "api", \
        help = "Feed from the api at API", metavar = "API", action = "append")
    parser.add_option("--service", dest = "service", \
        help = "Run as a service", action="store_true", \
        default=False)
    (options, args) = parser.parse_args()

    converter_path = os.path.abspath('converters')
    products_path = os.path.abspath('products')

    converters = converters.list(path = converter_path)

    inputs = []
    for path in (options.dirs + options.files):
        input = None
        if options.service:
            input = sources.file.watcher(path = dir)
        else:
            input = sources.file.indexer(path = dir)
        if input:
            inputs.append(input)
    for url in options.apis:
        input = None
        if options.service:
            input = sources.web.watcher(path = url)
        else:
            input = sources.web.indexer(path = url)
        if input:
            inputs.append(input)

    # Round-robin for now
    for input in inputs:
        for item in input.hopper():
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
