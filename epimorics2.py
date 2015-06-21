
import itertools

import utils
from rationals import Rational

primes = list(itertools.islice(utils.primes(), 100))



def getCodePair(code):
    return code > 0 and (code, code-1) or (-code-1, -code)
def formatCode(code):
    return "%d/%d" % getCodePair(code)
    
def getEpimoricWay(n0, n1):
    #"(6/5) -> [(3/2,1), (5/4,-1)]"
    #"(6/5) -> [(3,1), (5,-1)]"
    "(6/5) -> (3, -5)"
    result = ()
    r = Rational(n0, n1)
    while r != Rational(1):
        p, i = zip(primes, r)[-1]
        a = abs(i)
        s = i//a
        for j in range(a):
            result += (p * s,)
        r /= Rational(p, p-1) ** i
    return result



def getEpimoricSets(notes):                         # 4,5,6
    pairs = tuple(itertools.combinations(notes, 2)) # (4,5), (4,6), (5,6)
    print 'pairs (%d):' % len(pairs), pairs
    #
    result = {}
    for (n0,n1) in pairs:
        w = getEpimoricWay(n0,n1)
        result[(n0,n1)] = set(w)
        result[(n1,n0)] = set(-c for c in w)
    for k in result.keys(): print k, result[k]
    return result


       


class Tree(object):
    __slots__ = 'note','children'
    def __init__(self, note):
        self.note     = note
        self.children = []  # [(code,Tree)]
    def __str__(self):
        r = `self.note`
        if self.children:
            r += " (%s)" % ",".join("%s -> %s" % (formatCode(c), t) for (c,t) in self.children)
        return r


class Hole(object):
    __slots__ = 'sets','trees'
    def __init__(self, sets, trees):
        self.sets  = sets
        self.trees = trees
    def __str__(self):
        r = "Hole trees:\n" + "\n".join(" %s" % t for t in self.trees)
        r += "\n" + "sets:\n" + "\n".join(" %s: %s" % (k, " ".join(formatCode(c) for c in cs)) for (k,cs) in self.sets.items())
        return r



def makeStep(hole):
    print 'makeStep', hole
    notes = tuple(t.note for t in hole.trees)
    for note in notes:
        other = tuple(n for n in notes  if n != note)
        common = reduce(set.intersection, (hole.sets[(note,o)] for o in other))
        if common:
            code = common.pop()
            print 'step:', note, formatCode(code)
            #break
    
        
        


def findTrees(notes):
    sets  = getEpimoricSets(notes)
    trees = tuple(Tree(n) for n in notes)
    hole = Hole(sets, trees)
    makeStep(hole)
    


def test():
    #print [formatCodePair(code) for code in getEpimoricWay(15, 8)]
    notes = 4,5,6
    findTrees(notes)

if __name__ == "__main__":
    Rational.__repr__ = Rational.__str__
    test()

