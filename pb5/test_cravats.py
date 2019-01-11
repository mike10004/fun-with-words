#!/usr/bin/env python3

import os
import io
import sys
import logging
import unittest
from wordpal.puzzicon import Puzzeme
from pb5.cravats import WordProducer
import common.testing

_log = logging.getLogger(__name__)
common.testing.configure_logging()

class TestWordProducer(unittest.TestCase):

    def test_count_candidates_permute(self):
        test_cases = [
            (36, ('A', 'BC', 'DEF')),
            (24, ('AB', 'BC', 'G')),
        ]
        producer = WordProducer(permute=True)
        for expected, lettersets in test_cases:
            with self.subTest():
                self.assertEqual(expected, producer.count_candidates(lettersets), "expect count={} for {}".format(expected, lettersets))

    def test_produce_basic_permute(self):
        producer = WordProducer(permute=True)
        produced = []
        lettersets = ['A', 'BC', 'DEF']
        for word in producer.produce(lettersets):
            _log.debug("produced %s", word)
            self.assertIsInstance(word, str)
            self.assertEqual(len(lettersets), len(word), "each word produced must have length equal to number of lettersets")
            produced.append(word)
        self.assertEqual(36, len(produced))
        self.assertEqual(len(produced), len(set(produced)))

    def test_produce_dupes_no(self):
        producer = WordProducer(permute=True, allow_duplicates=False)
        produced = []
        lettersets = ['A', 'B', 'AC']
        for word in producer.produce(lettersets):
            _log.debug("produced %s", word)
            self.assertIsInstance(word, str)
            self.assertEqual(len(lettersets), len(word), "each word produced must have length equal to number of lettersets")
            produced.append(word)
        self.assertEqual(9, len(produced))
    
    def test_produce_dupes_yes(self):
        producer = WordProducer(permute=True, allow_duplicates=True)
        produced = []
        lettersets = ['A', 'B', 'AC']
        for word in producer.produce(lettersets):
            _log.debug("produced %s", word)
            self.assertIsInstance(word, str)
            self.assertEqual(len(lettersets), len(word), "each word produced must have length equal to number of lettersets")
            produced.append(word)
        self.assertEqual(12, len(produced))
    
    def test_restrict_perms(self):
        producer = WordProducer(permute=True, allow_duplicates=False, restrict_perms='B')
        produced = []
        lettersets = ['A', 'B', 'AC']
        for word in producer.produce(lettersets):
            _log.debug("produced %s", word)
            self.assertIsInstance(word, str)
            self.assertEqual(len(lettersets), len(word), "each word produced must have length equal to number of lettersets")
            produced.append(word)
        self.assertEqual(3, len(produced))

    def test_restrict_perms2(self):
        producer = WordProducer(permute=True, allow_duplicates=False, restrict_perms='B')
        produced = []
        lettersets = ['A', 'BD', 'AC']
        for word in producer.produce(lettersets):
            _log.debug("produced %s", word)
            self.assertIsInstance(word, str)
            self.assertEqual(len(lettersets), len(word), "each word produced must have length equal to number of lettersets")
            produced.append(word)
        self.assertEqual(3, len(produced))