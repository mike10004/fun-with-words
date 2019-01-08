#!/usr/bin/env python3

from __future__ import print_function
import sys
import logging
import random
from argparse import ArgumentParser

_BLANK = '_'
_ALPHABET = ''
_log = logging.getLogger('anagrammery_interactive')
_CMD_LAST = '/'
_CMD_EXIT = '/EXIT'
_CMD_SHUFFLE = '/SHUFFLE'
_CMD_ALPHABETIZE = '/ALPHABETIZE'
_ALIASES = {
    '/LAST': '/',
    '/QUIT': '/EXIT',
    '/ALPHA': '/ALPHABETIZE',
    '/A': '/ALPHABETIZE',
}
_SAMPLE_COMMANDS = tuple([c.lower() for c in (_CMD_SHUFFLE, _CMD_ALPHABETIZE, _CMD_EXIT)])


class LetterPool(object):

    def __init__(self, letters, num_blanks):
        self.letters = tuple(letters)
        self.original_num_blanks = num_blanks
        self.num_blanks = num_blanks
        self.used = []
        self.mode = 'strict'
    
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
    
    def get_unused(self):
        unused = list(self.letters)
        for lt in self.used:
            unused.remove(lt)
        return unused

    def consume(self, chars):
        strangers = []
        for ch in chars:
            if ch.strip():
                strange = False
                unused = self.get_unused()
                if not ch in unused:
                    if self.num_blanks > 0:
                        self.num_blanks -= 1
                    else:
                        strange = True
                        strangers.append(ch)
                if not strange or self.mode == 'lenient':
                    self.used.append(ch)
        if strangers:
            _log.info("\"used\" letters not in pool: %s", strangers)
    
    def shuffle(self):
        shuffled = list(self.letters)
        random.shuffle(shuffled)
        self.letters = shuffled
    
    def get_shuffled(self, n=None, subset=None):
        if n is None:
            shuffled = list(self.letters if subset is None else subset)
            random.shuffle(shuffled)
            return tuple(shuffled)
        else:
            return set([self.get_shuffled(subset=self.get_unused()) for i in range(n)])
    
    def alphabetize(self):
        alphabetized = sorted(self.letters)
        self.letters = alphabetized


def normalize_cmd(cmd):
    if cmd and cmd[0] == '/':
        splitted = cmd.split()
        cmd, params = splitted[0], splitted[1:]
    else:
        params = tuple()
    cmd = cmd.upper()
    try:
        cmd = _ALIASES[cmd]
    except KeyError:
        pass
    return cmd, params


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
            entry, params = normalize_cmd(input("consume: "))
            print()
            if entry == '/':
                entry = previous or ''
            if entry == '/EXIT':
                break
            elif entry == '/RESET':
                pool.reset()
            elif entry == '/SHUFFLE' or entry == '/S':
                if params:
                    n = int(params[0])
                    shuffles = pool.get_shuffled(n)
                    for s in shuffles:
                        print(''.join(s))
                    if len(shuffles) < n:
                        _log.info("more shuffles requested %s than available %s", n, len(shuffles))
                    print()
                else:
                    pool.shuffle()
            elif entry == _BLANK:
                print("using blanks not supported yet", file=sys.stderr)
            elif entry == _CMD_ALPHABETIZE:
                pool.alphabetize()
            elif entry and entry[0] == '/':
                print("command not recognized:", entry, file=sys.stderr)
            elif entry:
                pool.consume(entry)
            else:
                if not entry:
                    print("enter a letter or a command ({})".format(', '.join(_SAMPLE_COMMANDS)), file=sys.stderr)
                    continue
                raise ValueError(entry)
            previous = entry
    except KeyboardInterrupt:
        print("\nquitting now", file=sys.stderr)
        pass
    return 0            


if __name__ == '__main__':
    exit(main())
