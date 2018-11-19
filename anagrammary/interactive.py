#!/usr/bin/env python3

from __future__ import print_function
import sys
import logging
import random
from argparse import ArgumentParser

_BLANK = '_'
_ALPHABET = ''
_log = logging.getLogger('anagrammery_interactive')


class LetterPool(object):

    def __init__(self, letters, num_blanks):
        self.letters = tuple(letters)
        self.original_num_blanks = num_blanks
        self.num_blanks = num_blanks
        self.used = []
    
    @classmethod
    def build(cls, letters_token):
        letters_token = letters_token.upper()
        letters = ''.join(letters_token.split())  # remove whitespace
        clean_letters = [ch for ch in filter(lambda x: x != _BLANK, letters)]  # convert string to list of characters
        num_blanks = len(list(filter(lambda x: x == _BLANK, letters)))
        return LetterPool(clean_letters, num_blanks)
    
    def render(self):
        unused = list(self.letters)
        strangers = []
        for ch in self.used:
            try:
                unused.remove(ch)
            except ValueError:
                pass
        blanks = ['?' for i in range(self.num_blanks)]
        return "{} {}".format(' '.join(unused), ''.join(blanks))
    
    def reset(self):
        self.used.clear()
        self.num_blanks = self.original_num_blanks
    
    def consume(self, chars):
        strangers = []
        for ch in chars:
            if ch.strip():
                if not ch in self.letters:
                    if self.num_blanks > 0:
                        self.num_blanks -= 1
                    else:
                        strangers.append(ch)
                self.used.append(ch)
        if strangers:
            _log.info("\"used\" letters not in pool: %s", strangers)
    
    def shuffle(self):
        shuffled = list(self.letters)
        random.shuffle(shuffled)
        self.letters = shuffled


def main():
    p = ArgumentParser()
    p.add_argument("letters", help="pool of letters")
    p.add_argument("--log-level", choices=('DEBUG', 'INFO', 'WARN', 'ERROR'), default='INFO', help="set log level")
    args = p.parse_args()
    logging.basicConfig(level=logging.__dict__[args.log_level])
    pool = LetterPool.build(args.letters)
    previous = None
    try:
        while True:
            _log.debug("pool: %s (num_blanks = %s)", pool.letters, pool.num_blanks)
            print("pool:", pool.render())
            if pool.used:
                print("state:", ''.join(pool.used))
            print()
            entry = input("consume: ").upper()
            print()
            if entry == '/':
                entry = previous or ''
            if entry == '/EXIT':
                break
            elif entry == '/RESET':
                pool.reset()
            elif entry == '/SHUFFLE' or entry == '/S':
                pool.shuffle()
            elif entry == _BLANK:
                print("using blanks not supported yet", file=sys.stderr)
            elif entry and entry[0] == '/':
                print("command not recognized:", entry, file=sys.stderr)
            elif entry:
                pool.consume(entry)
            else:
                raise ValueError(entry)
            previous = entry
    except KeyboardInterrupt:
        print("\nquitting now", file=sys.stderr)
        pass
    return 0            


if __name__ == '__main__':
    exit(main())
