# Make unique based on a hash function 

def uniqify(values):
    hash_dict = {}
    for v in values:
        hash_dict[v.hash()] = v
    return list(hash_dict.values())
