
import itertools    # https://docs.python.org/2/library/itertools.html


class defaultlist(list):
    def __init__(self, default= 0):
        self.default = default
    def __getitem__(self, index):
        if len(self) <= index: return self.default
        return list.__getitem__(self, index)
    def __setitem__(self, index, value):
        while len(self) <= index: self.append(self.default)
        list.__setitem__(self, index, value)
        while self and self[-1] == self.default: del self[-1]  # minimize
    def clear(self):
        self[:] = []

def take(count, iters):
    for (i,x) in enumerate(iters):
        if i == count: break
        yield x

# math

def mult(xs):
    import operator
    return reduce(operator.mul, xs, 1)

def integers(start= 0):
    while True:
        yield start
        start += 1

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

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def factor(a):
    if a <= 0: return
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
    


# combinatorics

# see also https://docs.python.org/2/library/itertools.html


def variations(n, p):
    # find a better function name !!!
    "(3, 2) -> (0, 0, 0), (0, 0, 1),.. (1, 1, 1)"
    if n == 0:
        yield ()
    else:
        for v in variations(n-1, p):
            for i in range(p):
                yield v + (i,)


def combinations(items, size):
    # same as itertools.combinations
    # combinations('ABCD', 2) -> AB AC AD BC BD CD
    if size == 0:
        yield ()
    else:
        for i,item in enumerate(items):
            for c in combinations( items[i+1:], size-1 ):
                yield (item,) + c


def combinations_bits(n, k):
    # (5, 2) -> [(1,1,0,0,0), (1,0,1,0,0),..
    return (
        tuple((i in c and 1 or 0) for i in range(n))
            for c in combinations(range(n), k)
    )


def permutations_groups(groups):
    # ["AAA","B","CC"] -> ["AAABCC", "AAACBC",..
    
    def mix(g0, g1, bits):
        # ("AAA", "BB", [0,0,1,0,1]) -> "AABAB"
        r = []; i0 = 0; i1 = 0
        for b in bits:
            if b == 0:
                r.append(g0[i0]); i0 += 1
            else:
                r.append(g1[i1]); i1 += 1
        return tuple(r)
        
    def mix2(g0, g1):
        # ("AAA", "BB") -> ["AAABB", "AABAB",..
        return (mix(g0, g1, [1-b for b in bits]) for bits in combinations_bits(len(g0)+len(g1), len(g0)))

    result = [()]
    for g in groups:
        result = [m  for r in result  for m in mix2(r, g)]
    return result


def test():
    #for v in variations(3): print v

    #for c in combinations_bits(5, 2):
    #    print c
    
    for p in permutations_groups(["AAA","B","CC"]):
        print p

if __name__ == "__main__":
    test()
    
    

