
import math
import utils
import sonantometry  # http://sonantometry.blogspot.com/

class Rational(object):
    def __init__(self, *args):
        self.powers = utils.defaultlist()
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
            else:
                self.setPowers(args)

    def setPowers(self, powers):
        self.powers = utils.defaultlist()
        for p in powers:
            self.powers.append(p)

    def setFraction(self, n, d):
        self.powers = utils.defaultlist()
        for (i,p) in enumerate(utils.powers(n)):
            self.powers[i] += p
        for (i,p) in enumerate(utils.powers(d)):
            self.powers[i] -= p
    
    def setSonant(self, sonant):
        self.setPowers(sonantometry.sonantToPowers(sonant))
    
    def getSonant(self):
        return sonantometry.powersToSonant(self.powers)

    def getFraction(self, i= 3):
        n = 1; d = 1
        for (p,a) in zip(utils.primes(), self.powers):
            if   a > 0: n *= p**a
            elif a < 0: d *= p**(-a)
        return ("%%%dd" % i % n) + "/" + ("%%-%dd" % i % d)
    
    def getCents(self):
        f = 1.0
        for (p,a) in zip(utils.primes(), self.powers):
            f *= p ** a
        return math.log(f, 2) * 1200
    
    def __repr__(self):
        return self.getFraction(3)
        

def test():
    r = Rational('3/20')
    r = Rational(27, 20)
    print r, r.powers, r.getSonant(), r.getCents()
    

if __name__ == "__main__":
    test()
    
