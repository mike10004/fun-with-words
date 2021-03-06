#!/usr/bin/env python3

import os
import io
import sys
import logging
import unittest
from . import puzzicon
from .puzzicon import Puzzeme, Puzzarian
import common.testing

common.testing.configure_logging()

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
    
    def test_alphabet(self):
        self.assertEqual(26 * 2, len(puzzicon._ALPHABET))
        self.assertEqual(26 * 2, len(set(puzzicon._ALPHABET)))


class TestPuzzeme(unittest.TestCase):

    def test_canonicalize(self):
        c = Puzzeme.canonicalize("puzzle's\n")
        self.assertEqual('PUZZLES', c)

    def test_canonicalize_diacritics(self):
        c = Puzzeme.canonicalize(u'Málaga')
        self.assertEqual('MALAGA', c)

    def test_create(self):
        p = Puzzeme('a')
        self.assertEqual('A', p.canonical)
        self.assertEqual('a', p.rendering)
    
    def test_create_diacritics(self):
        p = Puzzeme(u'café')
        self.assertEqual('CAFE', p.canonical)


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
    
    def test_has_canonical(self):
        p = Puzzarian(_SIMPLE_PUZZEME_SET)
        self.assertTrue(p.has_canonical('baz'))
        self.assertTrue(p.has_canonical('Foo'))
        self.assertFalse(p.has_canonical('oranges'))


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
    
