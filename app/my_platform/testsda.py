import hashlib

def _createHash():
    """This function generate 10 character long hash"""
    hash = hashlib.sha1()
    return(hash.hexdigest()[:-10])
    

print(_createHash())

import random

hash = random.getrandbits(128)

print("%032x" % hash)