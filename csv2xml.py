#!/usr/bin/env python

import csv
import sys
import xml.dom.minidom
import xml.etree.ElementTree

class csv2xml:
    def __init__(self, filename):
        file = open(filename)

        sniffer = csv.Sniffer()
        sample = file.readline()
        file.seek(0)
        dialect = sniffer.sniff(sample)
        explicit = sniffer.has_header(sample)

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
    if len(sys.argv[1:]) == 0:
        print 'Syntax: ' + sys.argv[0] + ' <input file>'
    else:
        print csv2xml(filename = sys.argv[1])
