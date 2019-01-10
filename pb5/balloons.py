#!/usr/bin/env python3

import sys
import os
import logging
import argparse
import itertools
from wordpal import puzzicon

_log = logging.getLogger(__name__)
_BLANK = '?'


class WordSearcher(object):

    def __init__(self, puzzeme_set):
        self.puzzerarian = puzzicon.Puzzerarian(puzzeme_set)
    
    def find(self, balloons, num_balloons):
        assert isinstance(num_balloons, int) and num_balloons > 0, "target length must be a positive integer"
        balloons = [b.upper() for b in balloons]
        combos = itertools.combinations(balloons, num_balloons - 1)
        for combo in combos:
            _log.debug("examining balloon combo %s", combo)
            combo = list(combo) + [_BLANK]
            if len(combo) == num_balloons:
                for perm in itertools.permutations(combo, len(combo)):
                    pattern = ''.join(perm)
                    _log.debug("searching dictionary for pattern %s", pattern)
                    filters = [puzzicon.Filters.canonical_wildcard(pattern)]
                    for match in self.puzzerarian.search(filters):
                        yield match.canonical


