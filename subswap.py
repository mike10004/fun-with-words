#!/usr/bin/env python3

from __future__ import print_function
import sys
import re
from wordpal import puzzicon
from wordpal.puzzicon import Puzzarian

def find_transforms(puzzemes, fro, to, ofile=sys.stdout):
  puzzarian = Puzzarian(puzzemes)
  fro = fro.upper()
  def split_on(word):
    m = re.fullmatch(r'(\w*)' + fro + r'+?(\w*)', word)
    if m is not None:
      return m.group(1), m.group(2)
  valids = []
  for p in puzzemes:
    parts = split_on(p.canonical)
    if not parts:
      continue
    thword = parts[0] + to.upper() + parts[1]
    if puzzarian.has_canonical(thword):
      valids.append((p.canonical, thword))
      print(p.canonical + "\t" + thword, file=ofile)
  return valids

def main():
  args = sys.argv[1:]
  if len(args) != 2:
    print("exactly two arguments required: <FROM> <TO>", file=sys.stderr)
  fro, to = args[0], args[1]
  puzzemes = puzzicon.load_default_puzzemes()
  found = find_transforms(puzzemes, fro, to, sys.stdout)
  return 0 if found else 2

if __name__ == '__main__':
  exit(main())
