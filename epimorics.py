
import itertools

import utils
from rationals import Rational



def getEpimoricZip(r):
    "(6/5) -> [(3/2,1), (5/4,-1)]"
    result = []
    while r != Rational(1):
        p, i = zip(utils.primes(), r)[-1]
        e = Rational(p, p-1)
        result.insert(0, (e, i))
        r /= e ** i
    return result


def getEpimoricWays(r):                                    # 9/5 ->
    z = getEpimoricZip(r)                                  # [  (3/2,2) (5/4,-1) ]
    groups = [ [e ** (k/abs(k))] * abs(k) for (e,k) in z]  # [ [3/2, 3/2], [4/5] ]
    for perm in utils.permutations_groups(groups):         # [3/2, 3/2, 4/5], [3/2, 4/5, 3/2],..
        yield perm




class Step(object):
    def __init__(self, scala, note0, i0,i1, note1):
        self.scala = scala  # R
        self.note0 = note0  # R
        self.i0 = i0        # N
        self.i1 = i1        # N
        self.note1 = note1  # R
    def __str__(s):
        return "scala %s: %d (%s) -> %d (%s)" % (s.scala, s.i0, s.note0, s.i1, s.note1)

class Path(object):
    def __init__(self, r0,r1, way):
        self.r0 = r0
        self.r1 = r1
        self.way = way
        self.steps = getSteps(r0,r1, way)
    def __str__(self):
        return "path %s -> %s: %s" % (self.r0, self.r1, self.way)
    def getAllNotes(self):
        return (self.r0,) + tuple(s.note1 for s in self.steps)
    def getAllScalas(self):
        return tuple(set(s.scala for s in self.steps))


def getSteps(r0,r1, way):
    steps = []
    cur = r0
    for e in way:
        i0,i1 = e.getFraction()
        step = Step(cur/i0, cur, i0,i1, cur*i1/i0)
        steps.append(step)
        cur = step.note1
    if cur != r1: raise Exception("%s != %s", (cur, r1))
    return steps


def getPaths(r0,r1):
    return [Path(r0,r1, way) for way in getEpimoricWays(r0/r1)]


def formatPath(path):
    from collections import defaultdict
    #
    grid = defaultdict(defaultdict)
    for s in path.steps:
        grid[s.note0][s.scala] = s.i0
        grid[s.note1][s.scala] = s.i1
    #grid[r0][Rational(1)] = r0
    #grid[r1][Rational(1)] = r1
    #for i in sorted(grid.keys()): print i, dict(grid[i])
    
    # scalas
    scalas = []
    for row in grid.values():
        scalas += row.keys()
    scalas = sorted(set(scalas))
    gcd = Rational.gcd(*scalas)
    
    # table
    columns = sorted(set(scalas + [gcd]))
    table = []
    table.append([""] + [("(%s)" % str(j)) for j in columns])  # columns header
    for i in sorted(grid.keys())[::-1]:
        def cell(j):
            r = grid[i].get(j)
            if r is not None: return str(r)
            if j == gcd: return "[%s]" % str(i/gcd)
            return ""
        h = i in (path.r0, path.r1) and ">" or ""  # row header
        table.append([h] + [cell(j) for j in columns])
    #for row in table: print row

    # result
    widths = [max(len(row[j]) for row in table) for j in range(len(table[0]))]
    return "\n".join(" ".join(s.center(widths[j]) for (j,s) in enumerate(row)) for row in table)


class Chord(object):
    def __init__(self, notes, paths):
        self.notes = notes
        self.paths = paths
        # !!! make them lazy
        #self.gcd = Rational.gcd(self.notes)
        self.scalas = tuple(sorted(self.getAllScalas()))
    def __str__(self):
        r = "chord %s scalas %s" % (self.notes, self.scalas)
        for p in self.paths:
            r += "\n  %s" % p
        return r
    def getAllScalas(self):
        return tuple(set(
            s  for p in self.paths  for s in p.getAllScalas()
        ))
    def getAllNotes(self):
        return tuple(set(
            n  for p in self.paths  for n in p.getAllNotes()
        ))
    def isGcdBased(self):
        gcd = Rational.gcd(*self.notes)
        return all((s/gcd).isInteger() for s in self.scalas)
    def getRate(self):
        return (
            len(self.scalas),
            len(self.getAllNotes())
        )
    def getBestChains(self):
        if len(self.scalas) == 1:
            return [[self]]
        childChains = findBestChains(self.scalas)
        return [[self]+c for c in childChains]

def generateAllChords(notes):
    notes = map(Rational, notes)                # 4,5,6
    pairs = itertools.combinations(notes, 2)    # (4,5), (4,6), (5,6)
    paths = [getPaths(*p) for p in pairs]       # paths of (4,5), paths of (4,6), paths of (5,6)
    for ps in itertools.product(*paths):         # all interpretations
        yield Chord(notes, ps)

@utils.memoized
def findBestChains(notes):
    #print "findBestChains", notes
    chords = generateAllChords(notes)
    
    # filter by gcd
    chords = itertools.ifilter(lambda c: c.isGcdBased(), chords)
    
    # filter by rate
    chords = utils.findBestItems(chords, lambda c: c.getRate())
    
    # build chains
    chains = [chain   for chord in chords   for chain in chord.getBestChains()]
    
    # filter chains by size
    if len(chains) > 1:
        chains = utils.findBestItems(chains, lambda chain: len(chain))

    # filter chains by chord rate
    if len(chains) > 1:
        chains = utils.findBestItems(chains, lambda chain: tuple(chord.getRate() for chord in chain))

    # filter chains by all scales
    if len(chains) > 1:
        chains = utils.findBestItems(chains, lambda chain: len(set(s   for chord in chain   for s in chord.scalas)))

    return chains


def test():
    #r = Rational(21, 8)
    #r = Rational(9, 5)
    #r = Rational(81, 80)
    r0 = Rational(9)
    r1 = Rational(5)
    for path in getPaths(r0,r1):
        print "=" * 30
        print path.r0, "->", path.r1, "way", path.way
        for s in path.steps: print str(s)
        f = formatPath(path)
        if f:
            print
            print f

def test3():
    from chords import generateChords
    allNotes = utils.take(50, generateChords())
    for notes in allNotes:
        print "="*30, notes
        chains = findBestChains(notes)
        for chain in chains:
            for c in chain:
                print c
            print


if __name__ == "__main__":
    Rational.__repr__ = Rational.__str__
    test3()
