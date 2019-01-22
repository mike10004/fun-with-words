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
    parser.add_argument("-l", "--log-level", choices=('DEBUG', 'INFO', 'WARN', 'ERROR', 'debug', 'info', 'warn', 'error'), default='INFO', help="set log level")
    args = parser.parse_args()
    logging.basicConfig(level=logging.__dict__[args.log_level.upper()])
    letters = []
    specials = set()
    inputs, blankpools = lookup._remove_blankpools(' '.join(args.letters))
    for ch in inputs:
        ch = ch.upper()
        if ch in lookup._ALPHABET:
            letters.append(ch)
        elif ch not in lookup._BLANKS and ch  not in lookup._GARBAGE:
            _log.warn("invalid letter %s", ch)
    if not letters:
        _log.error("no valid letters provided")
        return 1
    puzzemes = puzzicon.load_default_puzzemes()
    if args.puzzeme_threshold is not None:
        evaluator = Evaluator()
        puzzemes = filter(lambda p: evaluator.evaluate(p) >= args.puzzeme_threshold, puzzemes)
    canonicals = map(lambda p: p.canonical, puzzemes)
    soothsayer = Soothsayer.build(canonicals)
    nlookups = 0
    found = set()
    for blankproduct in itertools.product(*blankpools):
        nlookups += 1
        word = ''.join(letters) + ''.join(blankproduct)
        answers = soothsayer.lookup(word)  # a set of tuples
        for answer in answers:   # answer is a tuple of strings
            joined = ' '.join(answer)
            if joined not in found:
                found.add(joined)
                print(joined)
    _log.debug("%d words found out of %d lookups", len(found), nlookups)
    if not found:
        _log.info("zero words found")
        return 1
    return 0
    

if __name__ == '__main__':
    exit(main())
