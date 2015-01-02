import unittest
from eunomia.models import Program, Rule, Atom, Term
from eunomia.engine import Engine
import eunomia.utils

class TestEngine(unittest.TestCase):

    def setUp(self):
        eunomia.utils.clear_tmp_parse_files()

    def test_engine_init(self):
        predicate1 = Term("p")
        constant1 = Term("a")
        var1 = Term("?x", True)
        atom1 = Atom(predicate1, [ constant1, var1 ])

        predicate2 = Term("q")
        constant2 = Term("b")
        var2 = Term("?y", True)
        atom2 = Atom(predicate2, [ constant2, var2 ])

        head = Atom(predicate1, [ constant1 ])

        rule1 = Rule(head, [atom1, atom2])
        rule2 = Rule(head, [atom1])
        rule3 = Rule(head, [])

        program = Program()
        program.add_rule(rule1)
        program.add_rule(rule2)
        program.add_fact(rule3)

        engine = Engine(program)

        self.assertEqual(engine.program, program)
        self.assertEqual(set(map(lambda x: x.hash(), engine.get_facts())), set([head.hash()]) )

    def test_load_program(self):
        program = eunomia.utils.load_program('examples/path.lp')
        self.assertTrue(len(program.rules), 2)
        engine = Engine(program)

        fact = Atom(Term("edge"), [ Term("a"), Term("b")])
        engine.push_fact(fact)
        results = engine.get_facts()

        self.assertTrue(len(results), 2)

        expected = []
        expected.append(str(Atom(Term("path"), [ Term("a"), Term("b")])))
        expected.append(str(Atom(Term("edge"), [ Term("a"), Term("b")])))
        self.assertEqual(set(map(lambda x: str(x), results)), set(expected))

        fact2 = Atom(Term("edge"), [ Term("c"), Term("d")])

        engine.push_fact(fact2)
        results = engine.get_facts()
        self.assertEqual(set(map(lambda x: str(x), results)), set(map(lambda x: str(x), [Atom(Term("edge"), [ Term("c"), Term("d")]), Atom(Term("edge"), [ Term("a"), Term("b")]), Atom(Term("path"), [ Term("a"), Term("b")]), Atom(Term("path"), [ Term("c"), Term("d")])])))

        # finally transitivity
        fact3 = Atom(Term("edge"), [ Term("b"), Term("c")])
        engine.push_fact(fact3)
        results = engine.get_facts()

        expected = []
        expected.append(Atom(Term("path"), [ Term("c"), Term("d")]))
        expected.append(Atom(Term("edge"), [ Term("a"), Term("b")]))
        expected.append(Atom(Term("edge"), [ Term("b"), Term("c")]))
        expected.append(Atom(Term("path"), [ Term("b"), Term("c")]))
        expected.append(Atom(Term("path"), [ Term("a"), Term("b")]))
        expected.append(Atom(Term("path"), [ Term("a"), Term("c")]))
        expected.append(Atom(Term("path"), [ Term("b"), Term("d")]))
        expected.append(Atom(Term("path"), [ Term("a"), Term("d")]))
        expected.append(Atom(Term("edge"), [ Term("c"), Term("d")]))

        self.assertEqual(set(map(lambda x: str(x), results)), set(map(lambda x: str(x), expected)))

    def test_ex_20150102(self):
        program = eunomia.utils.load_program('examples/ex_20150102.lp')
        engine = Engine(program)
        expected = ['r(b)', 'p(b)', 'q(b)', 's(a)', 'r(a)', 's(b)']
        self.assertEqual(set(map(str, engine.get_facts())), set(expected))

        query = Atom(Term("s"), [ Term("?x", True) ])
        matching = [ 's(a)', 's(b)'] 
        self.assertEqual(set(map(str, engine.get_matching_facts(query))), set(matching))





