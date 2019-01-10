#!/usr/bin/env python3

import os
import io
import sys
import logging
import unittest
from wordpal.puzzicon import Puzzeme
from pb5.balloons import WordSearcher

_log = logging.getLogger(__name__)
_logging_configured = False

if not _logging_configured:
    level_str = os.getenv('UNIT_TEST_LOG_LEVEL') or 'INFO'
    level = logging.__dict__.get(level_str, 'INFO')
    logging.basicConfig(level=level)
    _log.debug("logging configured at level %s (%s)", level, level_str)
    logging_configured = True


class TestWordSearcher(unittest.TestCase):

    def test_search(self):
        searcher = WordSearcher(frozenset([Puzzeme('foo'), Puzzeme('bar'), Puzzeme('baz')]))
        balloons = ('B', 'A', 'F', 'G')
        num_balloons = 3
        matches = set()
        for match in searcher.find(balloons, num_balloons):
            self.assertIsInstance(match, str)
            matches.add(match)
        self.assertSetEqual(set(['BAR', 'BAZ']), matches)


