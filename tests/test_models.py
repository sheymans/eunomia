import unittest
from eunomia.models import Program, Rule, Atom, Term

class TestModels(unittest.TestCase):
    
    def test_term(self):
        constant = Term("a")
        var = Term("?a", True)
        self.assertEqual(str(constant), "a")
        self.assertFalse(constant.is_var)
        self.assertEqual(str(var), "?a")
        self.assertTrue(var.is_var)

    def test_atom(self):
        predicate = Term("p")
        constant = Term("a")
        var = Term("?x", True)
        atom = Atom(predicate, [ constant, var ])
        self.assertEqual(str(atom), "p(a, ?x)")

    def test_rule(self):
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
        fact = Rule(head, [])

        self.assertEqual(str(rule1), "p(a) :- p(a, ?x), q(b, ?y).")
        self.assertEqual(str(rule2), "p(a) :- p(a, ?x).")
        self.assertEqual(str(fact), "p(a).")

    def test_program(self):
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
        fact = Rule(head, [])

        program = Program()
        program.add_rule(rule1)
        program.add_rule(rule2)
        program.add_rule(fact)

        self.assertEqual(str(program), "p(a) :- p(a, ?x), q(b, ?y).\np(a) :- p(a, ?x).\np(a).\n")

    def test_unify_with_ground(self):
        predicate1 = Term("p")
        constant1 = Term("a")
        var1 = Term("?x", True)
        atom1 = Atom(predicate1, [ constant1, var1 ])

        predicate2 = Term("p")
        constant2 = Term("a")
        constant3 = Term("c", True)
        atom2 = Atom(predicate2, [ constant2, constant3 ])

        mapping = atom1.unify_with_ground(atom2)
        self.assertEqual(len(mapping), 1)
        self.assertEqual(mapping['?x'].value, 'c') 

        atom3 = Atom(predicate2, [ var1, var1 ])

        mapping = atom3.unify_with_ground(atom2)
        self.assertFalse(mapping)

        atom4 = Atom(predicate2, [ constant1, constant1 ])
        mapping = atom3.unify_with_ground(atom4)
        self.assertEqual(len(mapping), 1)
        self.assertEqual(mapping['?x'].value, 'a') 


        var2 = Term("?y", True)
        atom5 = Atom(predicate1, [ var1, var2 ])
        mapping = atom5.unify_with_ground(atom2)
        self.assertEqual(len(mapping), 2)
        self.assertEqual(mapping['?x'].value, 'a') 
        self.assertEqual(mapping['?y'].value, 'c') 


        #for key in mapping:
        #    print "mapping ", key, " to ", mapping[key]

    def test_builtins_program(self):
        # test hash, eq, neq
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
        fact = Rule(head, [])

        program = Program()
        program.add_rule(rule1)
        program.add_rule(rule2)
        program.add_rule(fact)

        program2 = program

        self.assertEqual(type(program.hash()), int)
        self.assertTrue(program == program2)

        program2 = Program()
        self.assertTrue(program != program2)

    def test_fact(self):
        predicate1 = Term("p")
        constant1 = Term("a")

        head = Atom(predicate1, [ constant1 ])

        fact = Rule(head, [])

        self.assertTrue(fact.is_fact())

    def test_builtins_rule(self):
        predicate1 = Term("p")
        constant1 = Term("a")
        head = Atom(predicate1, [ constant1 ])
        fact = Rule(head, [])
        self.assertEqual(type(fact.hash()), int)

        fact2 = fact
        self.assertTrue(fact == fact2)
        fact2 = Rule(head, [head])
        self.assertTrue(fact != fact2)

    def test_builtins_atom(self):
        predicate1 = Term("p")
        constant1 = Term("a")
        head = Atom(predicate1, [ constant1 ])

        head2 = head
        self.assertTrue(head == head2)
        head2 = Atom(predicate1, [Term("b")])
        self.assertTrue(head != head2)

    
    def test_resolve_term(self):
        var = Term("?x", True)
        var2 = Term("?y", True)
        mapping = { '?x': Term("a") }

        self.assertEqual(var.resolve(mapping), Term("a"))
        self.assertEqual(var2.resolve(mapping), var2)


    def test_merge(self):
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
        fact = Rule(head, [])

        program = Program()
        program.add_rule(rule1)
        program.add_rule(rule2)
        program.add_rule(fact)

        self.assertEqual(str(program), "p(a) :- p(a, ?x), q(b, ?y).\np(a) :- p(a, ?x).\np(a).\n")

        # now program with just a fact:
        predicate3 = Term("r")
        constant3 = Term("a")
        at3 = Atom(predicate3, [ constant3 ])
        fact2 = Rule(at3, [])

        program2 = Program()
        program2.add_rule(fact2)
        # let's also add the fact as a fact (we'll have it double)
        program2.add_fact(fact2)

        self.assertEqual(str(program2), "r(a).\nr(a).")

        program.merge(program2)
        self.assertEqual(str(program), "p(a) :- p(a, ?x), q(b, ?y).\np(a) :- p(a, ?x).\np(a).\nr(a).\nr(a).")






























