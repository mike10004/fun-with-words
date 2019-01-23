import unittest
from anagrammary import lookup
from wordpal.puzzicon import Puzzeme
import logging
import common.testing
import itertools


_log = logging.getLogger(__name__)
common.testing.configure_logging()


class TestSoothsayer(unittest.TestCase):

    def test_lookup(self):
        s = lookup.Soothsayer.build(['SHALE', 'HEALS', 'HEELS', 'LEASH', 'HALEST', 'THEIR', 'THERE', 'WHERE', 'HERE'])
        self.assertSetEqual(set(), s.lookup(''))
        self.assertSetEqual(set([('SHALE',), ('HEALS',), ('LEASH',)]), s.lookup('ALESH'))
        self.assertSetEqual(set(), s.lookup('BOOGIE'))
        self.assertSetEqual(set([('WHERE',)]), s.lookup('HEWER'))

    def test_lookup_2word(self):
        s = lookup.Soothsayer.build(['A', 'B', 'C'], nwords=2)
        self.assertSetEqual(set(), s.lookup(''))
        actual = s.lookup('AB')
        _log.debug("lookup AB: %s", actual)
        self.assertSetEqual(set([('A', 'B'), ('B', 'A')]), actual)

    def test_lookup_2word_advanced(self):
        s = lookup.Soothsayer.build(['BOOK', 'WORM', 'BOOKWORM', 'FOO', 'BAR'], nwords=2)
        actual = s.lookup('WBOOROMK')
        _log.debug("lookup WBOOROMK: %s", actual)
        self.assertSetEqual(set([('BOOKWORM',), ('BOOK', 'WORM'), ('WORM', 'BOOK')]), actual)

    def test_lookup_2word_advanced2(self):
        s = lookup.Soothsayer.build(['REASON', 'ARE', 'SON', 'FOO', 'BAR'], nwords=2)
        actual = s.lookup('REASON')
        _log.debug("lookup REASON: %s", actual)
        self.assertSetEqual(set([('REASON',), ('ARE', 'SON'), ('SON', 'ARE')]), actual)

    
    def test_build_1word(self):
        canonicals = ['A', 'B', 'C']
        s = lookup.Soothsayer.build(canonicals, nwords=1)
        self.assertSetEqual(set(['A', 'B', 'C']), set(s.values()))
    
    def test_build_2word(self):
        canonicals = ['FOO', 'BAR', 'REASON', 'ARE', 'SON']
        s = lookup.Soothsayer.build(canonicals, nwords=2)
        ngrams = s.wordmap[181716194]
        _log.debug("ngrams with soul 181716194: %s", ngrams)
        self.assertEqual(3, len(ngrams))
        
    
    def test_build_2words_complex(self):
        canonicals = ['A', 'B']
        s = lookup.Soothsayer.build(canonicals, nwords=2)
        actual = set(s.values())
        _log.debug("wordmap values %s", actual)
        expected = ['A', 'B', 'A A', 'A B', 'B A', 'B B']
        self.assertSetEqual(set(expected), set(actual))


class TestTemplate(unittest.TestCase):

    def test_create(self):
        template = lookup.Template.create("ABC[DEF]GH?J[KL]")
        self.assertTupleEqual(tuple('ABCGHJ'), template.known_pool)
        expected_pools = list(itertools.product('DEF', lookup._ALPHABET, 'KL'))
        self.assertListEqual(expected_pools, list(template.iterate_unknowns()))

    def test_create_noblanks(self):
        template = lookup.Template.create("NOBLANKS")
        self.assertTupleEqual(tuple("NOBLANKS"), template.known_pool)
        self.assertEqual(1, template.count_unknown_combos())
        blankproducts = list(template.iterate_unknowns())
        self.assertListEqual([''], blankproducts)
    
    def test_iterate_possibles(self):
        template = lookup.Template.create("ABCDEF")
        actual = list(template.iterate_possibles())
        self.assertListEqual(['ABCDEF'], actual)


class TestModule(unittest.TestCase):

    def test__to_flat_list(self):
        test_cases = {
            'abc': ['a', 'b', 'c'],
            ('ab', 'cd', 'e'): ['a', 'b', 'c', 'd', 'e']
        }
        for arg, expected in test_cases.items():
            with self.subTest():
                self.assertListEqual(expected, lookup._to_flat_list(arg))
    
    def test_do_lookups_2words(self):
        provided = 'RNEOAS'
        puzzemes = set([Puzzeme('foo'), Puzzeme('bar'), Puzzeme('reason'), Puzzeme('are'), Puzzeme('son')])
        found = lookup.do_lookups(provided, puzzemes, max_words=2)
        _log.debug("found matching %s: %s", provided, found)
        expected = set(['REASON', 'ARE SON', 'SON ARE'])
        self.assertSetEqual(expected, found)

