#!/usr/bin/env python3

from __future__ import print_function
import io
import sys
import logging
import random
from argparse import ArgumentParser
from pb5.cravats import WordProducer
import wordpal.puzzicon
from wordpal.puzzicon import Puzzarian, Filters


_log = logging.getLogger(__name__)


def main():
    parser = ArgumentParser()
    parser.add_argument("lettersets", nargs='+', metavar="LETTERS")
    parser.add_argument("--permute", action='store_true', help="permute each candidate")
    parser.add_argument("-l", "--log-level", choices=('DEBUG', 'INFO', 'WARN', 'ERROR'), default='INFO', help="set log level")
    parser.add_argument("--count", action='store_true', help="only count the possibilities")
    parser.add_argument("--limit", type=int, help="check at most N candidates", metavar="N")
    parser.add_argument("--print-candidates", action='store_true')
    parser.add_argument("--allow-duplicates", action='store_true')
    parser.add_argument("--starts-with")
    args = parser.parse_args()
    logging.basicConfig(level=logging.__dict__[args.log_level])
    producer = WordProducer(permute=args.permute, allow_duplicates=args.allow_duplicates, restrict_perms=args.starts_with)
    lettersets = args.lettersets
    if args.count:
        count = producer.count_candidates(lettersets)
        print("{} possibilities for {} lettersets with lengths {}".format(count, len(lettersets), list(map(len, lettersets))))
    else:
        puzzemes = wordpal.puzzicon.load_default_puzzemes()
        puzzarian = Puzzarian(puzzemes)
        ncandidates, nwords = 0, 0
        for candidate in producer.produce(lettersets):
            ncandidates += 1
            if args.print_candidates:
                print(candidate, file=sys.stderr)
            if puzzarian.has_canonical(candidate):
                print(candidate)
                nwords += 1
            if args.limit is not None and ncandidates >= args.limit:
                break
        _log.debug("%d words out of %d candidates", nwords, ncandidates)
    return 0

if __name__ == '__main__':
    exit(main())