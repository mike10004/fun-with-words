from wordpal import puzzicon
from collections import defaultdict
from typing import Dict, Tuple, List, Set, Iterable


_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
_BLANKS = '?_.'
_GARBAGE = ' '
_DEFAULT_PENALTY = -50
_LETTER_SOULS = {
    'A': 2, 'B': 3, 'C': 5, 'D': 7, 'E': 11, 
    'F': 13,  'G': 17, 'H': 19, 'I': 23, 'J': 29, 
    'K': 31, 'L': 37,  'M': 41, 'N': 43, 'O': 47, 
    'P': 53, 'Q': 59, 'R': 61, 'S': 67, 'T': 71, 
    'U': 73, 'V': 79, 'W': 83, 'X': 89, 'Y': 97, 
    'Z': 101,
}


def compute_soul(word):
    soul = 1
    for ch in word.upper():
        p = _LETTER_SOULS[ch]
        soul *= p
    return soul


class Evaluator(object):

    def __init__(self, metrics=None):
        if metrics is None:
            metrics = [
                lambda rendering: "'" in rendering,
                lambda rendering: rendering[0].upper() == rendering[0]
            ]
        self.metrics = metrics
    
    def evaluate(self, puzzeme):
        aggregate = 0
        for metric in self.metrics:
            measurement = metric(puzzeme.rendering)
            if measurement is True:
                aggregate += _DEFAULT_PENALTY
            elif isinstance(measurement, int) or isinstance(measurement, float):
                aggregate += measurement
            else:
                raise ValueError("bad measurement by metric " + str(metric))
        return aggregate


class Soothsayer(object):

    def __init__(self, wordmap: Dict[int, List[Tuple[str, ...]]]):
        self.wordmap = wordmap
        assert isinstance(wordmap, dict), "wordmap must be a dictionary"

    @classmethod
    def build(cls, canonicals: Iterable[str], nwords=1):
        wordmap = defaultdict(list)
        for canonical in canonicals:
            soul = compute_soul(canonical)
            wordmap[soul].append((canonical,))
        if nwords > 1:
            raise NotImplementedError("multiple-word anagrams not yet implemented")
        return Soothsayer(wordmap)
    
    def lookup(self, word: str) -> Set[Tuple[str, ...]]:
        soul = compute_soul(word)
        try:
            return frozenset(self.wordmap[soul])
        except KeyError:  # allow for regular Dict in constructor
            return frozenset()


def _remove_blankpools(seq: str):
    chars = list(seq)
    blankpools = []
    clean_chars = []
    pool = None
    for ch in chars:
        if pool is None:
            if ch in _BLANKS:
                blankpools.append(_ALPHABET)
            elif ch == '[':
                pool = []
            else:
                clean_chars.append(ch)
        else:
            if ch == ']':
                blankpools.append(pool)
                pool = None
            else:
                pool.append(ch)
    blankpools = list(map(lambda pool: ''.join(pool), blankpools))
    return ''.join(clean_chars), blankpools
