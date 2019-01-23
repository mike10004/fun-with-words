#!/usr/bin/env python3

from __future__ import print_function
import re
import sys
import logging
from anagrammary.lookup import Soothsayer, Evaluator
from anagrammary import lookup
from wordpal import puzzicon
from argparse import ArgumentParser
import itertools


_log = logging.getLogger()


def main():
    parser = ArgumentParser()
    parser.add_argument("letters", nargs='*')
    parser.add_argument("--strict", dest="puzzeme_threshold", action='store_const', const=-10, help="restrict word list to simple words")
    parser.add_argument("-l", "--log-level", metavar="LEVEL", choices=('DEBUG', 'INFO', 'WARN', 'ERROR', 'debug', 'info', 'warn', 'error'), default='INFO', help="set log level")
    parser.add_argument("-m", "--max-words", type=int, default=1, metavar="N", help="max words per anagram")
    parser.add_argument("--dictionary", metavar="FILE", help="specify wordlist text file")
    args = parser.parse_args()
    logging.basicConfig(level=logging.__dict__[args.log_level.upper()])
    provided = ' '.join(args.letters)
    found = lookup.do_lookups(provided, args.dictionary, print, args.puzzeme_threshold, args.max_words)
    if not found:
        _log.info("zero words found")
        return 1
    return 0
   

if __name__ == '__main__':
    exit(main())
