#!/usr/bin/env python

from collections import Counter
import argparse

import sys


parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('-d',)
#parser.add_argument('-c',)
#parser.add_argument('-f',)
#parser.add_argument('-u',)
#parser.add_argument('-s',)
parser.add_argument('-i',)


uniques = Counter()

if __name__ == "__main__":
    if sys.argv[1:]:
        for file_name in sys.argv[1:]:
            with open(file_name) as file_handle:
                uniques.update(Counter(file_handle))
    else:
        uniques.update(Counter(sys.stdin))
    print uniques.most_common()


