#!/usr/bin/env python3

from collections import Counter
import argparse

import sys


parser = argparse.ArgumentParser(description='Worker out uniqueness')
parser.add_argument('-d',  dest='delimiter', metavar='D', type=str,
                    default=',', help='case insensitive output')
parser.add_argument('-C',  dest='comparator', type=str, default='Comparaison',
                    choices=('i', 'dp'))

uniques = Counter()

class Comparaison(object):
    def __init__(self, *args):
        pass

    def cmp(self, value1, value2):
        return value1 == value2
    

class IntComparaison(Comparaison):
    def cmp(self, value1, value2):
        return int(value1) == int(value2)


import math
class DecimalPlacesComparaison(Comparaison):
    def __init__(self, decimal_places):
        self.decimal_places = decimal_places

    def cmp(self, value1, value2):
        def parts(v):
            int_part = math.floor(float(v))
            fractional_part = float(v) - int_part
            relevant_fractional_part = round(fractional_part * 10 ** self.decimal_places)
            return (int_part, relevant_fractional_part)

        return parts(value1) == parts(value2)

class LineGenerator(object):

    def __init__(self, options, filehandle=None):
        self.options = options
        self.filehandle = filehandle if filehandle is not None else sys.stdin

    def __iter__(self):
        for line in self.filehandle:
            #yield line.split(self.options.delimiter)
            yield line


def comparable(value):
    comparator = DecimalPlacesComparaison(2)

    class Wrapper(object):
        def __init__(self, value):
            self.value = value

        def __eq__(self, other):
            return comparator.cmp(self.value, other.value)

        def __repr__(self):
            return self.value

        def __hash__(self):
            return 1

    return Wrapper(value)

def decimal_places_reduce(options, file_handle=None):
    for line in LineGenerator(options, file_handle):
        yield comparable(line.strip('\n'))

if __name__ == "__main__":
    if "test" in sys.argv:
        d = DecimalPlacesComparaison(2)
        assert d.cmp(3.14, 3.144)
        assert not d.cmp(3.14, 3.149)
        assert not d.cmp(2, 3)

    options = parser.parse_args()
    if sys.argv[1:]:
        for file_name in sys.argv[1:]:
            with open(file_name) as file_handle:
                uniques.update(Counter(decimal_places_reduce(options, file_handle)))
    else:
        uniques.update(Counter(decimal_places_reduce(options)))
    print (uniques.most_common())


