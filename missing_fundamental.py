
from collections import defaultdict

import utils
from rationals import Rational 


class Spectrum(defaultdict):
    def __init__(self, *items, **params):
        defaultdict.__init__(self, float)
        if items:
            weights = params.get("weights", [1.0] * len(items))
            for (i,a) in enumerate(items):
                if isinstance(a, Rational):
                    self[a] = weights[i]
                else:
                    self[Rational(a)] = weights[i]  # create Rational key by argument

    def getFundamentals(self):
        result = Spectrum()
        keys = sorted(self.keys(), key= float)  # might be not sorted
        variations = list(utils.variations(len(keys)))[1:]
        for v in variations:  # (0,0,1), (0,1,0), (0,1,1),.. (1,1,1)   
            ks = [k for (b,k) in zip(v, keys) if b]
            d = Rational.gcd(*ks)
            value = utils.mult( self[k] for k in ks )
            value **= 1.0/len(ks)  # geometric mean
            result[ d ] += value
        return result

    def printTable(self):
        for k in sorted(self.keys(), key= float):
            print k, self[k]

    def draw(self, initial= None):
        keys = sorted(self.keys(), key= float)
        d = Rational.gcd(*keys)
        for i in range(int(keys[0]/d), int(keys[-1]/d)+1):
            k = d * i
            w0 = initial and initial.get(k, 0)
            w1 = self.get(k, 0)
            print "%s %s%s%s %s" % (
                initial and ("%-8s" % (w0 or "")) or "",
                "%2d" % i,
                k.getFraction(5),
                "%-6s" % k.getSonant(),
                "%-8s" % (w1 or "")
            )


def drawFundamentals(*args, **kw):
    s = Spectrum(*args, **kw)
    f = s.getFundamentals()
    f.draw(s)
    print


def test():
    drawFundamentals("1/1", "5/4", "3/2")
    #drawFundamentals(10, 12, 15, weights= (1.0, 1.0, 1.0))
    #drawFundamentals("1/1", "6/5", "3/2", weights= (1.0, 1.0, 1.0))
    #drawFundamentals("1/1", "5/4", "3/2", "9/5")
    #drawFundamentals("1/1", "5/4", "3/2", "9/5", weights= (1.0, 1.0, 1.0, 0.2))
    drawFundamentals("1/1", "6/5", "3/2", "9/5", weights= (1.0, 1.0, 1.0, 0.2))
    #drawFundamentals("1/1", "2/1")


if __name__ == "__main__":
    test()
    