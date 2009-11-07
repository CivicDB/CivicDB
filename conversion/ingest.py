#!/usr/bin/env python

from __future__ import with_statement
import collections
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
    parser.add_option("-d", "--dir", dest = "dirs", \
        help = "Convert all files in DIR", metavar = "DIR", action = "append")
    parser.add_option("-f", "--file", dest = "files", \
        help = "Convert FILE", metavar = "FILE", action = "append")
    parser.add_option("--api", dest = "apis", \
        help = "Feed from the api at API", metavar = "API", action = "append")
    parser.add_option("--service", dest = "service", \
        help = "Run as a service", action="store_true", \
        default = False)
    (options, args) = parser.parse_args()

    converter_path = os.path.join(os.path.dirname(__file__), 'converters')
    products_path = os.path.join(os.path.dirname(__file__), 'products')

    converters = converters.list(path = converter_path)

    inputs = collections.deque()
    locals = []
    if options.dirs:
        locals += options.dirs
    if options.files:
        locals += options.files
    for path in locals:
        input = None
        if options.service:
            input = sources.file.watcher(path = path)
        else:
            input = sources.file.indexer(path = path)
        if input:
            inputs.append(input)
    remotes = []
    if options.apis:
        remotes += options.apis
    for url in remotes:
        input = None
        if options.service:
            input = sources.web.watcher(path = url)
        else:
            input = sources.web.indexer(path = url)
        if input:
            inputs.append(input)

    # Round-robin for now
    while len(inputs) > 0:
        input = inputs.popleft()
        dataset = input.next()
        if dataset:
            # Put the input source back in the queue, as it was not
            # empty.
            inputs.append(input)
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
