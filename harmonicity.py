
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

#---------------------------------

from utils import primes
from rationals import Rational

def mult(l):
    import operator
    return reduce(operator.mul, l, 1)

def tree(primes, check, level, r = ()):
    if r == ():
        if not check(1): return
    for p in primes():
        if level < p: break
        r1 = (p,) + r
        if not check(mult(r1)): return  # skip other primes
        tree(primes, check, p, r1)

def main():
    def check_denominator(D):
        d = Rational(1, D)
        h = HARMONIC_DISTANCE(d.powers)
        R0, R1 = numerator_range(D)
        #print "------------ denominator", fraction(d), "(%s)" % h, "nominator %d..%d" % (R0,R1)
        #trace_result()
        if result_distance and result_distance <= h: return False
        def co_primes():
            for (i,p) in enumerate(primes()):
                if d.powers[i] == 0: yield p  # skip primes used in denominator
        def check_numerator(N):
            #print N
            if N < R0: return True
            if N > R1: return False
            f = Rational(N, D)
            #print f, fraction(f), "(%s)" % HARMONIC_DISTANCE(f.powers)
            needed = add_result(f)
            return needed
        tree(co_primes, check_numerator, LEVEL)
        return True
    tree(primes, check_denominator, LEVEL)
    #print
    #trace_result()    
    print_result()
    
def numerator_range(D):
    import math
    return (int(math.ceil(RANGE[0] * D)),
            int(math.floor(RANGE[1] * D)))

result = []  # [(powers, distance)]
result_distance = 0
def add_result(r):
    global result, result_distance
    h = HARMONIC_DISTANCE(r.powers)
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
        print r[0].getFraction(),
    if result_distance: print " distance:", result_distance
    else: print

def print_result():
    rs = map(lambda r: (r[0], r[1], r[0].getCents()), result)
    rs.sort(key= lambda r: r[2])
    for (r,h,c) in rs:
        print "%14.8f %-10s %s %6.3f" % (c, r.getSonant(), r.getFraction(), h)
    
main()
