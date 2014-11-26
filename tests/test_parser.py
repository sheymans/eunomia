import unittest
from eunomia.parser import Parser
from eunomia.models import Term, Atom, Rule, Program

class TestParser(unittest.TestCase):
    

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

