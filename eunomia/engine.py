from index import FactIndex, RuleIndex
from models import Program, Rule, Atom, Term

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

        # Now add rules to index
        for rule in self.program.rules:
            # push rule (add to rule index, resolve against any facts, add new
            # rules)
            self.push_rule(rule)

        # Now add the base facts to the indices
        for fact in self.program.facts:
            # push this fact through (add to fact index, resolve against all matching rules,
            # deduce new facts).
            self.push_fact(fact)

    def push_rule(self, rule):
        # After resolution the original rule might now be trying to push a
        # rule that is essentially a fact (empty body)
        if rule.is_fact():
            self.rule_index.push_fact(rule.head)
        else:
            if not self.__in_register(rule):
                # it's not seen yet:
                self.__add_register(rule)
                self.rule_index.add_rule(rule)

                new_rules = self.fact_index.get_resolutions(rule)
                self.push_rules(new_rules)

    def push_fact(self, fact):
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
        for r in new_rules:
            self.push_rule(r)

    def get_facts(self):
        return self.fact_index.get_all_facts()
            
    # Private

    def __add_register(self, el):
        self.register[el.hash()]

    def __in_register(self, el):
        return el.hash() in self.register

