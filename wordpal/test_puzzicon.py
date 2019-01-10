#!/usr/bin/env python3

import os
import io
import sys
import logging
import unittest
from . import puzzicon
from .puzzicon import Puzzeme, Puzzarian

_log = logging.getLogger(__name__)
_logging_configured = False

if not _logging_configured:
    level_str = os.getenv('UNIT_TEST_LOG_LEVEL') or 'INFO'
    level = logging.__dict__.get(level_str, 'INFO')
    logging.basicConfig(level=level)
    _log.debug("logging configured at level %s (%s)", level, level_str)
    logging_configured = True


_DEFAULT_PUZZEME_SET = puzzicon.load_default_puzzemes()
_SIMPLE_PUZZEME_SET = puzzicon.create_puzzeme_set(['foo', 'bar', 'baz', 'gaw'])

class TestModuleMethods(unittest.TestCase):

    def test_read_default(self):
        self.assertNotEqual(0, len(_DEFAULT_PUZZEME_SET), "no puzzemes in default set")
    
    def test_create_filelike(self):
        wordlist = """apples
peaches
pumpkin"""
        ifile = io.StringIO(wordlist)
        puzzemes = puzzicon.create_puzzeme_set(ifile)
        self.assertSetEqual(set([Puzzeme('apples'), Puzzeme('peaches'), Puzzeme('pumpkin'),]), puzzemes)


class TestPuzzeme(unittest.TestCase):

    def test_canonicalize(self):
        c = Puzzeme.canonicalize("puzzle's\n")
        self.assertEqual('PUZZLES', c)

    def test_create(self):
        p = Puzzeme('a')
        self.assertEqual('A', p.canonical)
        self.assertEqual('a', p.rendering)


class TestPuzzerarian(unittest.TestCase):

    def test_search_many(self):
        p = Puzzarian(_DEFAULT_PUZZEME_SET)
        results = p.search([lambda p: p.canonical.startswith('PUZZ')])
        results = list(results)
        self.assertEqual(10, len(results))
    
    def test_search_one(self):
        p = Puzzarian(_DEFAULT_PUZZEME_SET)
        results = p.search([puzzicon.Filters.canonical('puzzle')], 0, 1)
        self.assertIsInstance(results, list)
        self.assertEqual(1, len(results))
        self.assertEqual('puzzle', results[0].rendering)


class TestFilters(unittest.TestCase):

    def test_canonical_literal(self):
        f = puzzicon.Filters.canonical('foo')
        self.assertTrue(f(Puzzeme('Foo')))
    
    def test_canonical_regex(self):
        f = puzzicon.Filters.canonical_regex(r'PU.ZLE')
        self.assertTrue(f(Puzzeme('puzzle')))
        self.assertFalse(f(Puzzeme('puzzles')))
        self.assertTrue(f(Puzzeme('pubzle')))
    
    def test_canonical_wildcard_q(self):
        f = puzzicon.Filters.canonical_wildcard('PU?ZLE')
        self.assertTrue(f(Puzzeme('puzzle')))
        self.assertFalse(f(Puzzeme('puzle')))
        self.assertFalse(f(Puzzeme('puzzles')))
        self.assertTrue(f(Puzzeme('pubzle')))
    
    def test_canonical_regex_star(self):
        f = puzzicon.Filters.canonical_wildcard('PU*ZLE')
        self.assertTrue(f(Puzzeme('puzzle')))
        self.assertTrue(f(Puzzeme('puzle')))
        self.assertFalse(f(Puzzeme('puzzles')))
        self.assertTrue(f(Puzzeme('pubzle')))
        self.assertTrue(f(Puzzeme('puabczle')))
    
