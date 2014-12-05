import unittest
from eunomia.index import AtomIndex
from eunomia.models import Atom, Term

class TestIndex(unittest.TestCase):
    
    def test_add(self):
        ind = AtomIndex()
        at = Atom(Term("p"), [Term("a"), Term("?x", True)])
        at2 = Atom(Term("p"), [Term("a"), Term("?y", True)])
        value = "random"
        value2 = "random2"

        ind.add(at, value)
        ind.add(at, value2)
        ind.add(at2, value2)

        # note that the index does not check for membership, we do this at the
        # Engine level
        self.assertEqual(ind.index, {'p': {'a': {-1: ['random', 'random2', 'random2']}}})

        at3 = Atom(Term("p"), [Term("a"), Term("d")])
        ind.add(at3, value)
        self.assertEqual(ind.index, {'p': {'a': {'d': ['random'], -1: ['random', 'random2', 'random2']}}})

    def test_get_values(self):
        ind = AtomIndex()
        at = Atom(Term("p"), [Term("a"), Term("?x", True)])
        at2 = Atom(Term("p"), [Term("a"), Term("?y", True)])
        value = "random"
        value2 = "random2"

        ind.add(at, value)
        ind.add(at, value2)
        ind.add(at2, value2)

        self.assertEqual(ind.get_values(at), ['random', 'random2', 'random2'])
        self.assertEqual(ind.get_values(at2), ['random', 'random2', 'random2'])

        at3 = Atom(Term("p"), [Term("a"), Term("d")])
        ind.add(at3, value)
        self.assertEqual(ind.get_values(at3), ['random' ])



