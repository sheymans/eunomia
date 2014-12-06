import os
from eunomia.parser import Parser
import os


# Make unique based on a hash function 
def uniqify(values):
    hash_dict = {}
    for v in values:
        hash_dict[v.hash()] = v
    return list(hash_dict.values())

def load_program(filename):
    program = None
    if os.path.isfile(filename):
        with open(filename, 'rU') as f:
            text = f.read()
            parser = Parser()
            program = parser.parse(text) 
    return program

 
