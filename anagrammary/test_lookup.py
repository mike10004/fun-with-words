import unittest
from anagrammary import lookup

class TestSoothsayer(unittest.TestCase):

    def test_lookup(self):
        s = lookup.Soothsayer.build(['SHALE', 'HEALS', 'HEELS', 'LEASH', 'HALEST', 'THEIR', 'THERE', 'WHERE', 'HERE'])
        self.assertSetEqual(set(), s.lookup(''))
        self.assertSetEqual(set([('SHALE',), ('HEALS',), ('LEASH',)]), s.lookup('ALESH'))
        self.assertSetEqual(set(), s.lookup('BOOGIE'))
        self.assertSetEqual(set([('WHERE',)]), s.lookup('HEWER'))
    

class TestModule(unittest.TestCase):

    def test__remove_blankpools(self):
        inputs, blankpools = lookup._remove_blankpools("ABC[DEF]GH?J[KL]")
        self.assertEqual('ABCGHJ', inputs)
        self.assertListEqual(['DEF', lookup._ALPHABET, 'KL'], blankpools)
