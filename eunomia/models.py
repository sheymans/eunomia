
class Program(object):
    """
    A Program keeps a list of its rules.
    """
    def __init__(self):
        # The original program is a list of rules and a list of facts
        self.rules = []
        self.facts = []
    
    def add_rule(self, rule):
        self.rules.append(rule)

    def add_fact(self, fact):
        self.facts.append(fact)

    def __str__(self):
        rules = "\n".join([str(rule) for rule in self.rules])
        facts = "\n".join([str(fact) for fact in self.facts])
        return rules + facts

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __ne__(self, other): 
        return not self == other

class Rule(object):
    """
    A Rule consists of a head atom and a possibly empty list of body atoms
    (body).
    """
    def __init__(self, head, body):
        # Head is a single atom, body is a list of atoms
        self.head = head
        self.body = body
    
    def __str__(self):
        result = str(self.head)
        if self.body:
            result += " :- "
            result += ", ".join([str(atom) for atom in self.body])
        return result + "."

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __ne__(self, other): 
        return not self == other

class Atom(object):
    """
    An Atom is of the form p(t1, ..., tn) where p is a predicate (a term) and ti are
    terms (possibly empty list).
    """
    def __init__(self, predicate, args):
        # for an atom p(t1, ..., tn) we have a predicate p and 
        # and a list of terms t1 ...tn as arguments
        # A predicate is a constant symbol
        self.predicate = predicate
        self.args = args

    def unify_with_ground(self, atom):
        """
        Try to unify this atom with another ground atom.
        Assumptions: (as we are not checking on it for speed)
            1. atom is indeed a ground atom.
            2. the predicates already match (we picked this atom and the atom up from indices that have to guarantee that).
            3. the constants on same argument positions already match
            4. the atoms have the same arity
        """
        mapping = {}
        for idx, a  in enumerate(self.args):
            if a.is_var:
                if a.value not in mapping:
                    mapping[a.value] = atom.args[idx] 
                elif mapping[a.value] != atom.args[idx]:
                    return False
                # else just skip
        # Return a mapping from values to terms.
        return mapping


    def __str__(self):
        result = str(self.predicate) + "("
        if self.args:
            result += ", ".join([str(term) for term in self.args])
        return result + ")"

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __ne__(self, other): 
        return not self == other

class Term(object):
    """
    A Term is a variable or a constant.
    """
    def __init__(self, value, is_var=False):
        # value of term is constant or variable, where the latter is assumed
        # to be always starting with a '?'
        self.value = value
        self.is_var = is_var

    def __str__(self):
        return str(self.value)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __ne__(self, other): 
        return not self == other
