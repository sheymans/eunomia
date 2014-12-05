import unittest
from eunomia.index import AtomIndex, RuleIndex, FactIndex
from eunomia.models import Atom, Term, Rule, Program

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

    def test_add_variable_first_argument(self):
        ind = AtomIndex()
        at = Atom(Term("p"), [Term("?x", True), Term("a")])
        ind.add(at, "random")
        self.assertEqual(ind.index, {'p': {-1: {'a': ['random']}}})

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

    def test_get_values_not_existing(self):
        ind = AtomIndex()
        at = Atom(Term("p"), [Term("a"), Term("?x", True)])
        at2 = Atom(Term("p"), [Term("a"), Term("b", False)])
        ind.add(at, "random") 

        self.assertFalse(ind.get_values(at2)) 

        # now wrong matching predicate ('q" was never inserted)
        at3 = Atom(Term("q"), [Term("a"), Term("b", False)])
        self.assertFalse(ind.get_values(at3))


    def test_get_more_general_matches(self):

        ind = AtomIndex()
        at = Atom(Term("p"), [Term("a"), Term("?x", True)])
        at2 = Atom(Term("p"), [Term("a"), Term("b", False)])
        ind.add(at, "random") 
        self.assertEqual(ind.get_more_general_matches(at2), ["random"])


        at3 = Atom(Term("q"), [Term("a"), Term("b", False)])
        self.assertEqual(ind.get_more_general_matches(at3), [])

    def test_get_more_general_matches_with_variable(self):

        ind = AtomIndex()
        at = Atom(Term("p"), [Term("a"), Term("?x", True)])
        ind.add(at, "random") 
        self.assertEqual(ind.get_more_general_matches(at), ["random"])

    def test_get_more_general_matches_none_present(self):

        ind = AtomIndex()
        at = Atom(Term("p"), [Term("a"), Term("?x", True)])
        at2 = Atom(Term("p"), [Term("b"), Term("c", True)])
        ind.add(at, "random") 
        self.assertEqual(ind.get_more_general_matches(at2), [])

    def test_get_more_specific_matches(self):

        ind = AtomIndex()
        at = Atom(Term("p"), [Term("a"), Term("?x", True)])
        at2 = Atom(Term("p"), [Term("a"), Term("b", False)])
        at3 = Atom(Term("p"), [Term("a"), Term("c", False)])
        ind.add(at2, "random") 
        ind.add(at3, "random2") 
        self.assertEqual(ind.get_more_specific_matches(at), ["random2", "random"])

        at4 = Atom(Term("q"), [Term("a"), Term("b", False)])
        self.assertEqual(ind.get_more_specific_matches(at4), [])

    def test_get_more_specific_matches_not_existing(self):

        ind = AtomIndex()
        at2 = Atom(Term("p"), [Term("a"), Term("b", False)])
        at3 = Atom(Term("p"), [Term("a"), Term("c", False)])
        ind.add(at2, "random") 
        self.assertEqual(ind.get_more_specific_matches(at3), [])

    def test_get_all_values(self):
        ind = AtomIndex()
        at = Atom(Term("p"), [Term("a"), Term("?x", True)])
        at2 = Atom(Term("p"), [Term("a"), Term("b", False)])
        at3 = Atom(Term("p"), [Term("a"), Term("c", False)])
        ind.add(at, Term("random")) 
        ind.add(at2, Term("random2")) 
        ind.add(at3, Term("random3")) 
        self.assertEqual(map(lambda x: x.value, ind.get_all_values()), ["random", "random2", "random3"])

        # now add duplicate
        ind.add(at3, Term("random3")) 
        # result should be the same:
        self.assertEqual(map(lambda x: x.value, ind.get_all_values()), ["random", "random2", "random3"])


    def test_add_rule(self):
        at = Atom(Term("p"), [Term("a"), Term("?x", True)])
        at2 = Atom(Term("p"), [Term("a"), Term("b", False)])
        at3 = Atom(Term("q"), [Term("a"), Term("c", False)])

        rule = Rule(at, [at2, at3])

        ind = RuleIndex()
        ind.add_rule(rule)

        self.assertEqual(ind.index.get_values(at2), [(0, rule)])
        self.assertEqual(ind.index.get_values(at3), [(1, rule)])

    def test_get_resolutions_ruleindex(self):
        at = Atom(Term("p"), [Term("a"), Term("?x", True)])
        at2 = Atom(Term("p"), [Term("a"), Term("b", False)])
        at3 = Atom(Term("q"), [Term("a"), Term("c", False)])

        rule = Rule(at, [at2, at3])

        ind = RuleIndex()
        ind.add_rule(rule)

        self.assertEqual(str(ind.get_resolutions(at3)[0]), "p(a, ?x) :- p(a, b).")
        self.assertEqual(str(ind.get_resolutions(at2)[0]), "p(a, ?x) :- q(a, c).")

    def test_get_resolutions_factindex(self):
        at = Atom(Term("p"), [Term("a"), Term("?x", True)])
        at2 = Atom(Term("p"), [Term("a"), Term("b", False)])
        at3 = Atom(Term("q"), [Term("a"), Term("c", False)])

        ind = FactIndex()
        ind.add_fact(at2)

        rule = Rule(at, [at2, at3])

        self.assertEqual(str(ind.get_resolutions(rule)[0]), "p(a, ?x) :- q(a, c).")

        # now also add at3
        ind.add_fact(at3)

        # we should now have 2 resolved rules:
        self.assertEqual(str(ind.get_resolutions(rule)[0]), "p(a, ?x) :- q(a, c).")
        self.assertEqual(str(ind.get_resolutions(rule)[1]), "p(a, ?x) :- p(a, b).")

    def test_get_all_facts(self):

        at = Atom(Term("p"), [Term("a"), Term("?x", True)])
        at2 = Atom(Term("p"), [Term("a"), Term("b", False)])
        at3 = Atom(Term("q"), [Term("a"), Term("c", False)])
        
        ind = FactIndex()
        ind.add_fact(at2)
        ind.add_fact(at3)

        self.assertEqual(ind.get_all_facts(), [at2, at3])
    



