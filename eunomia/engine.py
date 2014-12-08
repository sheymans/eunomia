from eunomia.index import FactIndex, RuleIndex
from eunomia.models import Program, Rule, Atom, Term

class Engine(object):
    
    def __init__(self, program):
        
        # store the original program
        self.program = program

        # an index of rules for fast resolution
        self.rule_index = RuleIndex()

        # an index of ground facts
        self.fact_index = FactIndex()


        # A register of rules and facts in the system, to be able to check
        # existence fast.
        self.register = {}

        # Now add rules and facts to index and resolve
        self.push_program(self.program)

    def push_rule(self, rule):
        # After resolution the original rule might now be trying to push a
        # rule that is essentially a fact (empty body)
        if rule.is_fact():
            self.push_fact(rule.head)
        else:
            if not self.__in_register(rule):
                # it's not seen yet:
                self.__add_register(rule)
                self.rule_index.add_rule(rule)

                new_rules = self.fact_index.get_resolutions(rule)
                self.push_rules(new_rules)

    def push_fact(self, fact):
        # fact is assumed to be an atom
        if not self.__in_register(fact):
            # it's not seen yet:
            self.__add_register(fact)
            self.fact_index.add_fact(fact)

            # now get all resolved rules with that fact.
            new_rules = self.rule_index.get_resolutions(fact)
            # and mutually recurse by pushing these new rules:
            # Note that some of these rules might be facts now (because of
            # resolution)
            self.push_rules(new_rules)

    def push_rules(self, rules):
        for r in rules:
            self.push_rule(r)

    def push_facts(self, facts):
        for f in facts:
            self.push_fact(f.head)

    def push_program(self, program):
        self.push_rules(program.rules)
        self.push_facts(program.facts)

    def get_facts(self):
        return self.fact_index.get_all_facts()
            
    # Private

    def __add_register(self, el):
        self.register[el.hash()] = 1

    def __in_register(self, el):
        return el.hash() in self.register

