#!/usr/bin/env python3

from __future__ import print_function
import sys
import logging
from argparse import ArgumentParser
from anagrammary import LetterPool, _BLANK, _CMD_ALPHABETIZE, normalize_cmd, _SAMPLE_COMMANDS

_log = logging.getLogger()


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
