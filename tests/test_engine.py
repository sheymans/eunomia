import unittest
from eunomia.models import Program, Rule, Atom, Term
from eunomia.engine import Engine

class TestEngine(unittest.TestCase):
    
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

        program = Program()
        program.add_rule(rule1)
        program.add_rule(rule2)
        program.add_fact(head)

        engine = Engine(program)

        self.assertEqual(engine.program, program)
        self.assertEqual(set(engine.get_facts()), set([head]) )



