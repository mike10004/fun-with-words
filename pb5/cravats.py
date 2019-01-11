import itertools
import logging
import math

_log = logging.getLogger(__name__)

class WordProducer(object):

    def __init__(self, **kwargs):
        self.permute = False
        self.allow_duplicates = False
        self.restrict_perms = None
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def calc_product_size(self, lettersets):
        n = 1
        for s in lettersets:
            n *= len(s)
        return n
    
    def count_candidates(self, lettersets):
        factor = 1 if not self.permute else math.factorial(len(lettersets))
        return factor * self.calc_product_size(lettersets)
    
    @classmethod
    def _remove_one(cls, combo, element):
        if element not in combo:
            return combo
        copy = list(combo)
        copy.remove(element)
        return copy
    
    def produce(self, lettersets):
        _log.debug("expect %s candidates from %d lettersets with lengths: %s", self.count_candidates(lettersets), len(lettersets), [len(s) for s in lettersets])
        used = set()
        cartesian = itertools.product(*lettersets)
        if self.permute:
            if self.restrict_perms:
                for combo in cartesian:
                    unrestricted = WordProducer._remove_one(combo, self.restrict_perms)
                    for tail in itertools.permutations(unrestricted):
                        value = self.restrict_perms + ''.join(tail)
                        if value in used:
                            continue
                        if not self.allow_duplicates:
                            used.add(value)
                        yield value
            else:
                for combo in cartesian:
                    for seq in itertools.permutations(combo):
                        value = ''.join(seq)
                        if value in used:
                            continue
                        if not self.allow_duplicates:
                            used.add(value)
                        yield value
        else:
            for seq in cartesian:
                value = ''.join(seq)
                if value in used:
                    continue
                if not self.allow_duplicates:
                    used.add(value)
                yield value
