
import math, collections
import utils
import sonantometry  # http://sonantometry.blogspot.com/

class Rational(utils.defaultlist):
    def __init__(self, *args):
        utils.defaultlist.__init__(self, 0)
        if len(args) == 2:
            self.setFraction(args[0], args[1])
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                if arg[0] == ':':
                    self.setSonant(arg)
                elif '/' in arg:
                    nd = arg.split('/', 1)
                    self.setFraction(int(nd[0]), int(nd[1]))
            elif hasattr(arg, '__iter__'):
                self.setPowers(arg)
            else:
                self.setFraction(arg, 1)

    def __eq__(a, b): return tuple(a) == tuple(b)
    def __ne__(a, b): return tuple(a) != tuple(b)
    def __lt__(a, b):
        n,d = (a/b).getFraction()
        return n < d

    def __hash__(self):
        return hash(tuple(self))
    def __float__(self):
        f = 1.0
        for (p,a) in zip(utils.primes(), self):
            f *= p ** a
        return f
    def __int__(self):
        return int(float(self))
    def __repr__(self):
        return "[%s]" % ",".join(`p` for p in self)
    def __str__(self):
        return self.formatFraction(1)
    
    #def __add__(a, b)
    #def __sub__(a, b)
    def __mul__(a, b):
        if not isinstance(b, Rational): return a * Rational(b)
        return Rational( p+q for (p,q) in Rational.zip(a, b) )
    def __div__(a, b):
        if not isinstance(b, Rational): return a / Rational(b)
        return Rational( p-q for (p,q) in Rational.zip(a, b) )
    def __pow__(a, i):
        return Rational(map(lambda k: k*i, a))

    def setPowers(self, powers):
        self.clear()
        for (i,p) in enumerate(powers):
            self[i] = p

    def setFraction(self, n, d):
        if n == 0 or d == 0: raise Exception("Invalid rational %d/%d" % (n,d))
        self.clear()
        for (i,p) in enumerate(utils.powers(n)):
            self[i] += p
        for (i,p) in enumerate(utils.powers(d)):
            self[i] -= p

    def setSonant(self, sonant):
        self.setPowers(sonantometry.sonantToPowers(sonant))
    
    def getSonant(self):
        return sonantometry.powersToSonant(self)

    def getFraction(self):
        n = 1; d = 1
        for (p,a) in zip(utils.primes(), self):
            if   a > 0: n *= p**a
            elif a < 0: d *= p**(-a)
        return (n, d)
    
    def formatFraction(self, i= 3):
        n, d = self.getFraction()
        result = "%%%dd" % i % n
        if d != 1:
            result += "/" + ("%%-%dd" % i % d)
        return result
    
    def getCents(self):
        return math.log( float(self), 2 ) * 1200
    
    def isInteger(self):
        return all(p >= 0 for p in self)
    
    @staticmethod
    def zip(*rs):
        for i in range(max(map(len, rs))):
            yield tuple(r[i] for r in rs)
            
    @staticmethod
    def gcd(*rs):
        return Rational(map(min, Rational.zip(*rs)))


def test():
    r = Rational('3/20')
    r = Rational(27, 20)
    print r, r, r.getSonant(), r.getCents()
    
    rs = Rational(1, 1), Rational(6, 5), Rational(3, 2)
    print rs[0], rs[1], rs[2], " -> ", Rational.gcd(*rs)
    #   1/1     6/5     3/2    ->    1/10 
    
    print Rational(3) / 10 * 4  #  6/5


def test2():
    r = Rational(77, 68)


if __name__ == "__main__":
    test2()
    
