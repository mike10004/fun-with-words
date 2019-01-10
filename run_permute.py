#!/usr/bin/env python3

from __future__ import print_function
import io
import sys
import logging
import random
from argparse import ArgumentParser


class Permutation(object):

    def __init__(self, original, mapping):
        self.original = original
        self.mapping = mapping
    
    def transform(self, query):
        outcome = io.StringIO()
        for i in range(len(query)):
            mi = self.original.find(self.mapping[i])
            print(query[mi], end="", file=outcome)
        return outcome.getvalue()


def main():
    p = ArgumentParser()
    p.add_argument("original")
    p.add_argument("mapping")
    p.add_argument("query")
    args = p.parse_args()
    xform = Permutation(args.original, args.mapping)
    outcome = xform.transform(args.query)
    print(outcome)
    return 0

if __name__ == '__main__':
    exit(main())