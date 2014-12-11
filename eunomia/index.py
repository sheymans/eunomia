import eunomia.utils

class AtomIndex(object):
    """
    Index where keys are atom patterns (variables are all treated as -1)
    """

    def __init__(self):
        self.index = {}

    def add(self, atom, value):
        pred = atom.predicate.value
        if pred not in self.index:
            self.index[pred] = {}
        self.__add_args(self.index[pred], atom.args, value)

    def get_values(self, atom):
        pred = atom.predicate.value
        if pred not in self.index:
            return []
        else:
            return self.__find(self.index[pred], atom.args)

    def get_more_general_matches(self, atom):
        """
        Get all values for all keys that match the atom, where a match is any generalization of the atom.
        """
        pred = atom.predicate.value
        if pred not in self.index:
            return []
        else:
            return self.__find_more_general(self.index[pred], atom.args)

    def get_more_specific_matches(self, atom):
        """
        Get all values for all keys that match the atom, where a match is any specialization of the atom.
        """
        pred = atom.predicate.value
        if pred not in self.index:
            return []
        else:
            return self.__find_more_specific(self.index[pred], atom.args)

    def get_all_values(self):
        """
        Get all unique values stored in the index.
        """
        def traverse(dic):
            if dic and type(dic) == dict:
                values = []
                for key in dic:
                    values.extend(traverse(dic[key]))
                return values
            else:
                return dic
        values = traverse(self.index)
        # values may contain duplicates. Just create a dict of hashes
        return eunomia.utils.uniqify(values)

    ## Private functions
    def __add_args(self, dic, args, value):
        if len(args) > 1:
            el = args[0]
            if el.is_var:
                key_val = -1
            else:
                key_val = el.value

            if key_val not in dic:
                dic[key_val] = {}
            self.__add_args(dic[key_val], args[1:], value)

        elif len(args) == 1:
            el = args[0]
            if el.is_var:
                key_val = -1
            else:
                key_val = el.value
            if key_val not in dic:
                dic[key_val] = [value]
            # elif value not in dic[key_val]:
            else:
                # we just append (no checking for duplicates, we assume for
                # speed that this gets done at the register level -- see
                # Engine)
                dic[key_val].append(value) 

    def __find(self, dic, args):
        if len(args) > 0:
            el = args[0]
            if el.is_var:
                key_val = -1
            else:
                key_val = el.value

            if key_val not in dic:
                return []
            else:
                return self.__find(dic[key_val], args[1:])
        elif type(dic) == list:
            return dic
        else:
            return []

    def __find_more_general(self, dic, args):
        """
        Find values for keys that are more general than args.
        """
        if len(args) > 0:
            el = args[0]
            key_val1 = key_val2 = None
            if el.is_var:
                # only generalization is variable  -1
                key_val1 = -1
            else:
                # generalize constant to both variable and constant
                key_val1 = -1
                key_val2 = el.value
            
            if key_val1 not in dic and key_val2 not in dic:
                return []
            else:
                values1 = []
                values2 = []
                if key_val1 in dic:
                    values1 = self.__find_more_general(dic[key_val1], args[1:])
                if key_val2 and key_val2 in dic:
                    values2 = self.__find_more_general(dic[key_val2], args[1:])
                return values1 + values2
        elif type(dic) == list:
            return dic
        else:
            return []

    def __find_more_specific(self, dic, args):
        """
        Find values for keys that are more specific than args. Specific means it has to be constants.
        """
        if len(args) > 0:
            el = args[0]
            key_val =  None
            if not el.is_var:
                # specialized value is value itself
                key_val = el.value 
                
            if key_val and key_val not in dic:
                return []
            elif key_val and key_val in dic:
                return self.__find_more_specific(dic[key_val], args[1:])

            else:
                # el is a var so all constant keys would be specializations
                values = []
                for key in dic:
                    if key != -1: # -1 is var
                        values.extend(self.__find_more_specific(dic[key], args[1:]))
                return values

        elif type(dic) == list:
            return dic
        else:
            return []

    ## Built-ins
    def __str__(self):
        return str(self.index)


class RuleIndex(object):
    """
    This is an AtomIndex storing rules using each of its body atoms as keys.
    The values are of the form (idx, rule) where idx indicates the index of the
    key in the rule.  This allows us to do fast resolution on each body atom.
    """
    
    def __init__(self):
        self.index = AtomIndex()

    def add_rule(self, rule):
        # for each of the body atoms we add this rule to the index.
        body = rule.body
        for idx, body_atom in enumerate(body):
            self.index.add(body_atom, (idx, rule))

    def get_resolutions(self, fact):
        # for the ground fact, get all rules in the index that have some body
        # atom that unifies with the fact. Return that rule and the mapping the
        # makes up the unification.
        candidate_idx_rule_pairs = self.index.get_more_general_matches(fact)

        # candidate_idx_rule_pairs is a list with items (x, rule) where x is
        # the index in the body of the rule that matches with fact.
        resolutions = []
        for (idx, rule) in candidate_idx_rule_pairs:
            mapping = rule.body[idx].unify_with_ground(fact)
            if mapping is not False:
                # resolution applys the mapping and remove the body atom at idx
                new_rule = rule.resolve(idx, mapping)
                # we could optimize here by pushing immediately for resolution
                # against facts.
                resolutions.append(new_rule)
        return resolutions

    ## Built-ins
    def __str__(self):
        return str(self.index)

class FactIndex(object):
    """
    This is an AtomIndex storing all facts. The key is the fact, the value is a
    singleton list of that fact.
    """
    def __init__(self):
        self.index = AtomIndex()

    def add_fact(self, fact):
        self.index.add(fact, fact)

    def get_resolutions(self, rule):
        """
        Get all new rules that result for matching ground facts in the fact index with any rule body atom.
        """
        resolutions = []
        for idx, body_atom in enumerate(rule.body):
            candidates = self.index.get_more_specific_matches(body_atom)

            for cand in candidates:
                mapping = body_atom.unify_with_ground(cand)
                if mapping is not False:
                    new_rule = rule.resolve(idx, mapping)
                resolutions.append(new_rule)
        return resolutions

    def get_all_facts(self):
        """
        Get all facts currently known to fact index.
        """
        return self.index.get_all_values()

    def get_matching_facts(self, atom):
        """
        Get all facts that match the atom (answer the query).
        """
        candidates = self.index.get_more_specific_matches(atom)

        # now only retain those candidates that actually unify (the indexes do
        # not distinguish between equal variables)

        facts = []
        for cand in candidates:
            mapping = atom.unify_with_ground(cand)
            if mapping is not False:
                new_fact = atom.resolve(mapping)
                facts.append(new_fact)
        return facts



    ## Built-ins
    def __str__(self):
        return str(self.index)



