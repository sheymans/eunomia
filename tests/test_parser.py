import unittest
from eunomia.parser import Parser
from eunomia.models import Term, Atom, Rule, Program
import os

class TestParser(unittest.TestCase):
    
    def setUp(self):
        if os.path.isfile('parser.out'):
            os.remove('parser.out')
        if os.path.isfile('parsetab.py'):
            os.remove('parsetab.py')
        if os.path.isfile('parsetab.pyc'):
            os.remove('parsetab.pyc')

    def test_parse_term_constant(self):
        self.parser = Parser('term')
        result = self.parser.parse("a")
        self.assertEqual(str(result), "a")
        self.assertEqual(type(result), Term)
        self.assertFalse(result.is_var)

    def test_parse_term_var(self):
        self.parser = Parser('term')
        result = self.parser.parse("?a")
        self.assertEqual(str(result), "?a")
        self.assertEqual(type(result), Term)
        self.assertTrue(result.is_var)

    def test_parse_atom(self):
        self.parser = Parser('atom')
        result1 = self.parser.parse("p(a)")
        self.assertEqual(str(result1), "p(a)")
        self.assertEqual(type(result1), Atom)
        self.assertEqual(result1.predicate, Term("p"))
        self.assertEqual(result1.args, [Term("a")])

    def test_parse_atom2(self):
        self.parser = Parser('atom')
        result1 = self.parser.parse("p(a, b)")
        self.assertEqual(str(result1), "p(a, b)")
        self.assertEqual(type(result1), Atom)
        self.assertEqual(result1.predicate, Term("p"))
        self.assertEqual(result1.args, [Term("a"), Term("b")])

    def test_parse_atoms(self):
        self.parser = Parser('atoms')
        result1 = self.parser.parse("p(a, b), q(c,d)")
        self.assertEqual(str(result1[0]), "p(a, b)")
        self.assertEqual(str(result1[1]), "q(c, d)")

    def test_parse_rule_fact(self):
        self.parser = Parser('rule')
        result1 = self.parser.parse("p(a, b).")
        self.assertEqual(type(result1), Rule)
        self.assertEqual(str(result1.head), "p(a, b)")
        self.assertEqual(result1.body, [])

    def test_parse_rule(self):
        self.parser = Parser('rule')
        result1 = self.parser.parse("p(a, b) :- q(c,d), r(e,f).")
        self.assertEqual(type(result1), Rule)
        self.assertEqual(str(result1.head), "p(a, b)")
        self.assertEqual(str(result1), "p(a, b) :- q(c, d), r(e, f).") 
        self.assertEqual(len(result1.body), 2)

    def test_parse_rules(self):
        self.parser = Parser('rules')
        result1 = self.parser.parse("p(a, b) :- q(c,d), r(e,f). p(c,d).")
        self.assertEqual(len(result1), 2)
        for rule in result1:
            self.assertEqual(type(rule), Rule)

        self.assertEqual(str(result1[0]), "p(a, b) :- q(c, d), r(e, f).") 
        self.assertEqual(str(result1[1]), "p(c, d).") 

    def test_parse_program(self):
        self.parser = Parser('program')
        result1 = self.parser.parse("p(a, b) :- q(c,d), r(e,f). p(c,d).")
        self.assertEqual(type(result1), Program)
        for rule in result1.rules:
            self.assertEqual(type(rule), Rule)

        self.assertEqual(str(result1.rules[0]), "p(a, b) :- q(c, d), r(e, f).") 
        self.assertEqual(str(result1.facts[0]), "p(c, d).") 

    def test_parse_program_fact(self):
        self.parser = Parser('program')
        result1 = self.parser.parse("p(a, b).")
        self.assertEqual(type(result1), Program)
        self.assertFalse(result1.rules)
        self.assertTrue(result1.facts)
        for fact in result1.facts:
            self.assertEqual(type(fact), Rule)

        self.assertEqual(str(result1.facts[0]), "p(a, b).") 





