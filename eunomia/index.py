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
            return None
        else:
            return self.__find(self.index[pred], atom.args)

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
            elif value not in dic[key_val]:
                dic[key_val].append(value) 

    def __find(self, dic, args):
        if len(args) > 0:
            el = args[0]
            if el.is_var:
                key_val = -1
            else:
                key_val = el.value

            if key_val not in dic:
                return None
            else:
                return self.__find(dic[key_val], args[1:])
        else:
            return dic

    ## Built-ins
    def __str__(self):
        return str(self.index)
