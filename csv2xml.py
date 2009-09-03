#!/usr/bin/env python

import sys
import csv
import xml

class csv2xml:
    def __init__(self, filename):
        self.file = open(filename)
        self.data = csv.DictReader(self.file)
    def __del__(self):
        self.file.close()
    def __repr__(self):
        out = '<data>\n'
        for entry in self.data:
            out += '  <entry>\n'
            for key in entry.keys():
                out += '    <field name = "' + key
                out += '" value = "' + entry[key] + '" />\n'
            out += '  </entry>\n'
        out += '</data>'
        return out

if __name__ == '__main__':
    if len(sys.argv[1:]) == 0:
        print 'Syntax: ' + sys.argv[0] + ' <input file>'
    else:
        print csv2xml(filename = sys.argv[1])
