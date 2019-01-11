#!/usr/bin/env python3

import os
import io
import sys
import logging
import unittest
from wordpal.puzzicon import Puzzeme
from pb5.balloons import WordSearcher
import common.testing

common.testing.configure_logging()

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


