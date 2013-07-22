

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

def variations(n, p= 2):
    # find a better function name !!!
    "(3, 2) -> (0, 0, 0), (0, 0, 1),.. (1, 1, 1)"
    if n == 0:
        yield ()
    else:
        for v in variations(n-1, p):
            for i in range(p):
                yield v + (i,)


def combinations(items, size):
    if size == 0:
        yield ()
    else:
        for i,item in enumerate(items):
            for c in combinations( items[i+1:], size-1 ):
                yield (item,) + c


def test():
    for v in variations(3): print v
    

if __name__ == "__main__":
    test()
    
    

