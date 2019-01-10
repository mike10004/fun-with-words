#!/usr/bin/env python3

import sys
import os
import logging
import argparse
from wordpal import puzzicon
from pb5.balloons import WordSearcher

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("balloons", nargs='+')
    parser.add_argument("-l", "--log-level", choices=('DEBUG', 'INFO', 'WARN', 'ERROR'), default='INFO', help="set log level")
    parser.add_argument("-v", "--verbose", action='store_const', const='DEBUG', dest='log_level', help="set log level DEBUG")
    parser.add_argument("-n", "--length", type=int, default=3)
    args = parser.parse_args()
    logging.basicConfig(level=logging.__dict__[args.log_level])
    searcher = WordSearcher(puzzicon.read_puzzeme_set())
    balloons = list()
    for b in args.balloons:
        if b.startswith('@'):
            with open(b[1:], 'r') as ifile:
                for line in ifile:
                    for x in line.split():
                        balloons.append(x.strip())
        else:
            balloons.append(b.strip())
    assert balloons, "no balloons provided"
    matches = searcher.find(balloons, args.length)
    for match in matches :
        print(match)
    return 0

if __name__ == '__main__':
    exit(main())
