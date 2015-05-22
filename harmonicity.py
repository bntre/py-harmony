#--------------------------------- Harmonic distances

import math
import utils

def euler(powers):
    return 1 + sum( abs(a) * (p-1) 
        for (p,a) in zip(utils.primes(), powers))

def barlow(powers):
    return sum( abs(a) * 2.0 * (p-1)**2/p
        for (p,a) in zip(utils.primes(), powers))

def simple(k):
    def h(powers):
        return sum( a**2 * p**k
             for (p,a) in zip(utils.primes(), powers))
    return h

def epimoric(k):
    def h(powers):
        z = Rational(powers).getEpimoricZip()
        return sum( a**2 * p**k
             for (p,a) in z)
    return h


#---------------------------------

from rationals import Rational

class RangeSearcher(object):
    def __init__(self, range, count, level, harmonic_distance):
        self.range = range
        self.count = count  # count of notes to find
        self.level = level  # JI limit level
        self.harmonic_distance = harmonic_distance  # function
        # result
        self.result_distance = 0
        self.result = []  # [(Rational, distance)]
    
    @staticmethod
    def tree(primes, check, level, r = ()):
        if r == ():
            if not check(1): return
        for p in primes():
            if level < p: break  # ugly !!!
            r1 = (p,) + r
            if not check(utils.mult(r1)): return  # skip other primes
            RangeSearcher.tree(primes, check, p, r1)

    def search(self):
        def check_denominator(D):
            d = Rational(1, D)
            h = self.harmonic_distance(d)
            R0 = int(math.ceil(self.range[0] * D))
            R1 = int(math.floor(self.range[1] * D))
            #print "------------ denominator", fraction(d), "(%s)" % h, "nominator %d..%d" % (R0,R1)
            #trace_result()
            if self.result_distance and self.result_distance <= h: return False
            def check_numerator(N):
                #print N
                if N < R0: return True
                if N > R1: return False
                f = Rational(N, D)
                #print f, fraction(f), "(%s)" % HARMONIC_DISTANCE(f)
                needed = self.add_result(f)
                return needed
            def co_primes():
                for (i,p) in enumerate(utils.primes()):
                    if d[i] == 0: yield p  # skip primes used in denominator
            self.tree(co_primes, check_numerator, self.level)
            return True
        self.tree(utils.primes, check_denominator, self.level)
        #print
        #trace_result()    
        self.print_result()

    def add_result(self, r):
        h = self.harmonic_distance(r)
        if self.result_distance and self.result_distance <= h: return False  # not needed
        self.result.append((r, h))
        #print "add_result", r, h
        self.result.sort(key = lambda p: float(p[1]))
        if len(self.result) >= self.count:
            self.result = self.result[:self.count]
            self.result_distance = self.result[-1][1]
            #print "result_distance", self.result_distance
        #self.trace_result()
        return True
    
    def trace_result(self):
        print "result:",
        for r in self.result:
            print r[0].getFraction(),
        if self.result_distance: print " distance:", self.result_distance
        else: print
    
    def print_result(self):
        maxdistance = max(r[1] for r in self.result)
        self.result.sort(key= lambda r: float(r[0]))
        for (r,h) in self.result:
            print "%14.8f %-10s %s %9.3f %s" % (r.getCents(), r.getSonant(), r.getFraction(), h, "#" * int(20 - 20*h/maxdistance))
        

def test():
    #RangeSearcher((1, 2), 30, 19, barlow).search()
    #RangeSearcher((1, 2), 30, 19, simple(4.0)).search()
    RangeSearcher((1, 2), 30, 19, epimoric(2.0)).search()
    
    #harmonic_distance = simple(5.0)
    #for i in range(1, 100):
    #    powers = utils.powers(i)
    #    print i, harmonic_distance(powers)


if __name__ == "__main__":
    test()
