#!/usr/bin/env python

from collections import Counter
import argparse

import sys


parser = argparse.ArgumentParser(description='Worker out uniqueness')
parser.add_argument('-d',  dest='delimiter', metavar='D', type=str,
                    default=',', help='case insensitive output')

uniques = Counter()


class LineGenerator(object):

    def __init__(self, options, filehandle=None):
        self.options = options
        self.filehandle = filehandle if filehandle is not None else sys.stdin

    def __iter__(self):
        for line in self.filehandle:
            yield tuple(line.split(self.options.delimiter))


if __name__ == "__main__":
    options = parser.parse_args()
    if sys.argv[1:]:
        for file_name in sys.argv[1:]:
            with open(file_name) as file_handle:
                uniques.update(Counter(LineGenerator(options, file_handle)))
    else:
        uniques.update(Counter(LineGenerator(options)))
    print uniques.most_common()


