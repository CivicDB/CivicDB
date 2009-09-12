#!/usr/bin/env python

import csv
import optparse
import sys
import xml.dom.minidom
import xml.etree.ElementTree

class csv2xml:
    def __init__(self, filename, test):
        file = open(filename)

        if test:
            sample1 = file.readline()
            sample2 = file.readline()
            file.close()
            if sample1.count(',') != sample2.count(','):
                sys.exit(1)
            if sample1.count(',') == 0:
                sys.exit(1)
            sys.exit(0)

        sniffer = csv.Sniffer()
        sampleblock = file.read(1024)
        file.seek(0)
        sampleline = file.readline()
        file.seek(0)
        dialect = sniffer.sniff(sampleblock)
        explicit = sniffer.has_header(sampleline)

        self._raw = csv.DictReader(file, restval = None, dialect = dialect)
        self._result = xml.etree.ElementTree.Element('data')
        for entry in self._raw:
            newentry = xml.etree.ElementTree.SubElement(self._result, 'entry')
            for key in entry.keys():
                # Allow for missing values 
                if entry[key]:
                    newfield = xml.etree.ElementTree.SubElement(newentry, 'field')
                    newfield.set(key = 'name', value = key)
                    newfield.set(key = 'value', value = entry[key])
        file.close()
    def __del__(self):
        pass
    def __repr__(self):
        return xml.dom.minidom.parseString(
            xml.etree.ElementTree.tostring(self._result)).toprettyxml()

if __name__ == '__main__':
    usage = 'usage: %prog [options] filename'
    parser = optparse.OptionParser(usage = usage)
    parser.add_option('--test', action = 'store_true', default = False, 
        dest = 'testonly',
        help = 'do not perform conversion, but decide if conversion is likely')
    (options, args) = parser.parse_args(sys.argv[1:])
    if len(args) == 0:
        parser.error()
        sys.exit(1)
    else:
        print csv2xml(filename = args[0], test = options.testonly)
        sys.exit(0)
