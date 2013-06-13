
RANGE = (1, 2)
#RANGE = (5/4.0, 4/3.0)
COUNT = 30      # count of notes to find
LEVEL = 19      # JI limit level

def HARMONIC_DISTANCE(r):
    #return euler(r)
    #return barlow(r)
    return simple(5.0, r)

#--------------------------------- Harmonic distances

def euler(powers):
    return 1 + sum( abs(a) * (p-1) 
        for (p,a) in zip(primes(), powers))

def barlow(powers):
    return sum( abs(a) * 2.0 * (p-1)**2/p
        for (p,a) in zip(primes(), powers))

def simple(k, powers):
    return sum( a**2 * p**k
        for (p,a) in zip(primes(), powers))

#--------------------------------- Utils

import math, operator

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

def mult(l):
    return reduce(operator.mul, l, 1)

class defaultlist(list):
    def __init__(self, d= 0):
        self.d = d
    def __getitem__(self, index):
        if len(self) <= index: return self.d
        return list.__getitem__(self, index)
    def __setitem__(self, index, value):
        while len(self) <= index: self.append(self.d)
        list.__setitem__(self, index, value)

def powers(fs):  # e.g. (2,2,2,2,  5,5, 7) -> [4,0,2,1]
    ps = defaultlist()
    for (i,p) in enumerate(primes()):
        ps[i] = list(fs).count(p)
        fs = filter(lambda a: a != p, fs)
        if not fs: break
    return ps

def divide(n, d):  # e.g. (1,0,0)/(0,0,1) -> (1,0,-1)
    f = defaultlist()
    s = max(len(n), len(d))
    for i in range(s):
        f[i] = n[i] - d[i]
    return f

def cents(r):
    f = 1.0
    for (p,a) in zip(primes(), r):
        f *= p ** a
    return math.log(f, 2) * 1200
    
def fraction(r):
    n = 1; d = 1
    for (p,a) in zip(primes(), r):
        if   a > 0: n *= p**a
        elif a < 0: d *= p**(-a)
    return ("%3s" % n) + "/" + ("%-3s" % d)


# http://sonantometry.blogspot.com/
def sonant(r):
    def code_(c, a):
        if a == 1: return c
        return `a` + c
    def code(c, a):
        if a > 0: return code_(c, a)
        if a < 0: return code_(c.lower(), -a)
        return ""
    codes = "TDMQNRPUVWZ" + "?"*20  # http://www.forumklassika.ru/showthread.php?t=18080&p=1367263&viewfull=1#post1367263
    return ":" + ("".join(code(c,a) for (c,a) in zip(codes,r)) or "0")

#--------------------------------- 

def tree(primes, check, level, r = ()):
    if r == ():
        if not check(r): return
    for p in primes():
        if level < p: break
        r1 = (p,) + r
        if not check(r1): return  # skip other primes
        tree(primes, check, p, r1)

def main():
    def check_denominator(dd):
        D = mult(dd)
        d = powers(dd)
        h = HARMONIC_DISTANCE(d)
        R0, R1 = numerator_range(D)
        #print "------------ denominator", fraction(d), "(%s)" % h, "nominator %d..%d" % (R0,R1)
        #trace_result()
        if result_distance and result_distance <= h: return False
        def co_primes():
            for (i,p) in enumerate(primes()):
                if d[i] == 0: yield p  # skip primes used in denominator
        def check_numerator(nn):
            N = mult(nn)
            #print N
            if N < R0: return True
            if N > R1: return False
            n = powers(nn)
            f = divide(n, d)  # fraction
            #print f, fraction(f), "(%s)" % HARMONIC_DISTANCE(f)
            needed = add_result(f)
            return needed
        tree(co_primes, check_numerator, LEVEL)
        return True
    tree(primes, check_denominator, LEVEL)
    #print
    #trace_result()    
    print_result()
    
def numerator_range(D):
    return (int(math.ceil(RANGE[0] * D)),
            int(math.floor(RANGE[1] * D)))

result = []  # [(powers, distance)]
result_distance = 0
def add_result(r):
    global result, result_distance
    h = HARMONIC_DISTANCE(r)
    if result_distance and result_distance <= h: return False  # not needed
    result.append((r, h))
    #print "add_result", r, fraction(r), h
    result.sort(key = lambda p: p[1])
    if len(result) >= COUNT:
        result = result[:COUNT]
        result_distance = result[-1][1]
        #print "result_distance", result_distance
    #trace_result()
    return True

def trace_result():
    print "result:",
    for r in result:
        print fraction(r[0]),
    if result_distance: print " distance:", result_distance
    else: print

def print_result():
    rs = map(lambda r: (r[0], r[1], cents(r[0])), result)
    rs.sort(key= lambda r: r[2])
    for (r,h,c) in rs:
        print "%14.8f %-10s %s %6.3f" % (c, sonant(r), fraction(r), h)
    
main()
