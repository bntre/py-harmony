

class defaultlist(list):
    def __init__(self, default= 0):
        self.default = default
    def __getitem__(self, index):
        if len(self) <= index: return self.default
        return list.__getitem__(self, index)
    def __setitem__(self, index, value):
        while len(self) <= index: self.append(self.default)
        list.__setitem__(self, index, value)



# math

def primes(): # http://code.activestate.com/recipes/117119/
    D = {}
    q = 2
    while True:
        if q not in D:
            yield q
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        q += 1

def factor(a):
    for p in primes():
        while True:
            if a == 1: return
            if a % p != 0: break  # next prime
            a /= p
            yield p

def powers(a):
    factors = list(factor(a))
    for (i,p) in enumerate(primes()):
        yield factors.count(p)
        factors = filter(lambda a: a != p, factors)
        if len(factors) == 0: break
    

