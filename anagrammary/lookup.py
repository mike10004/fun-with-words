from wordpal import puzzicon
from collections import defaultdict
from typing import Dict, Tuple, List, Set, Iterable, Callable
import logging
import itertools
import sys


_log = logging.getLogger(__name__)
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


def _NOOP(*args, **kwargs):
    pass


def _to_flat_list(blah):
    if isinstance(blah, str):
        return list(blah)
    else:
        lists = [list(x) for x in blah]
        master = []
        for l in lists:
            master += l
        return master


def compute_soul(word):
    soul = 1
    for ch in _to_flat_list(word):
        ch = ch.upper()
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
        assert nwords <= 3, "anagrams must be at most 3 words"
        _log.debug("building word map (max words %d)", nwords)
        wordmap = defaultdict(list)
        if nwords > 1:
            canonicals = list(canonicals)
        for canonical in canonicals:
            soul = compute_soul(canonical)
            wordmap[soul].append((canonical,))
        if nwords > 1:
            for i in range(nwords - 1):
                _log.debug("building dimension %d of word map", i + 2)
                wordmap_values = list(wordmap.values())
                for ngrams in wordmap_values:
                    for ngram in ngrams:
                        for canonical in canonicals:
                            newgram = tuple(list(ngram) + [canonical])
                            soul = compute_soul(newgram)
                            wordmap[soul].append(newgram)
        _log.debug("%d souls in word map", len(wordmap))
        return Soothsayer(wordmap)
    
    def lookup(self, word: str) -> Set[Tuple[str, ...]]:
        soul = compute_soul(word)
        try:
            return frozenset(self.wordmap[soul])
        except KeyError:  # allow for regular Dict in constructor
            return frozenset()
    
    def values(self):
        inner_joiner = lambda value: ' '.join(value)
        for ngrams in self.wordmap.values():
            for ngram in ngrams:
                yield ' '.join(ngram)


class Template(object):

    def __init__(self, known_pool, unknown_pools):
        self.known_pool = tuple(known_pool)
        self.unknown_pools = tuple(unknown_pools)
        self.length = len(self.known_pool) + len(self.unknown_pools)
    
    def iterate_unknowns(self):
        if self.unknown_pools:
            return itertools.product(*(self.unknown_pools))
        else:
            return ['']
    
    def iterate_possibles(self):
        blankproducts = self.iterate_unknowns()
        for blankproduct in blankproducts:
            _log.debug("yielding %s + %s", self.known_pool, blankproduct)
            combo = ''.join(self.known_pool) + ''.join(blankproduct)
            yield combo
    
    def count_unknown_combos(self):
        product = 1
        for pool in self.unknown_pools:
            product *= len(pool)
        return product

    @classmethod
    def create(cls, seq: str):
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
        clean_chars = ''.join(clean_chars)
        blankpools = list(map(lambda pool: ''.join(pool), blankpools))
        return Template(clean_chars, blankpools)
    
    def empty(self) -> bool:
        return len(self.known_pool) == 0 and len(self.unknown_pools) == 0


def do_lookups(provided: str, dictionary=None, callback:Callable=None, puzzeme_threshold:int=None, max_words:int=1):
    callback = callback or _NOOP
    template = Template.create(provided)
    found = set()
    if template.empty():
        _log.warn("no valid letters provided")
        return found
    if dictionary is None:
        puzzemes = puzzicon.load_default_puzzemes()
    elif isinstance(dictionary, set):
        puzzemes = dictionary
    else:
        if dictionary == '-':
            puzzemes = puzzicon.create_puzzeme_set(sys.stdin)
        else:
            puzzemes = puzzicon.read_puzzeme_set(dictionary)
    if puzzeme_threshold is not None:
        evaluator = Evaluator()
        puzzemes = filter(lambda p: evaluator.evaluate(p) >= puzzeme_threshold, puzzemes)
    canonicals = map(lambda p: p.canonical, puzzemes)
    soothsayer = Soothsayer.build(canonicals, nwords=max_words)
    nlookups, ndupes = 0, 0
    for word in template.iterate_possibles():
        nlookups += 1
        answers = soothsayer.lookup(word)  # a set of tuples
        for answer in answers:   # answer is a tuple of strings
            joined = ' '.join(answer)
            if joined not in found:
                found.add(joined)
                print(joined)
            else:
                _log.debug("duplicate %s", joined)
                ndupes += 1
    _log.debug("%d words found out of %d lookups (%d duplicates)", len(found), nlookups, ndupes)
    return found
