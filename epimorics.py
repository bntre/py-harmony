
import itertools

import utils
from rationals import Rational

primes = list(itertools.islice(utils.primes(), 100))

def getEpimoricZip(r):
    #"(6/5) -> [(3/2,1), (5/4,-1)]"
    "(6/5) -> [(3,1), (5,-1)]"
    result = []
    while r != Rational(1):
        p, i = zip(primes, r)[-1]
        result.insert(0, (p, i))
        r /= Rational(p, p-1) ** i
    return result


def getEpimoricWays(r):                                    # 9/5 ->
    z = getEpimoricZip(r)                                  # [  (3[/2],2) (5[/4],-1) ]
    #groups = [ [e ** (k/abs(k))] * abs(k) for (p,k) in z]  # [ [3/2, 3/2], [4/5] ]
    groups = [ [(p, k/abs(k))] * abs(k) for (p,k) in z]  # [ [3/2, 3/2], [4/5] ]
    for perm in utils.permutations_groups(groups):         # [3/2, 3/2, 4/5], [3/2, 4/5, 3/2],..
        yield perm




class Step(object):
    __slots__ = 'scala','note0','i0','i1','note1'
    def __init__(self, scala, note0, i0,i1, note1):
        self.scala = scala
        self.note0 = note0
        self.i0 = i0
        self.i1 = i1
        self.note1 = note1
    def __str__(s):
        return "scala %s: %d (%s) -> %d (%s)" % (s.scala, s.i0, s.note0, s.i1, s.note1)

def getSteps(n0,n1, way):
    steps = []
    cur = n0
    for (p,i) in way:
        #i0,i1 = e.getFraction()
        i0,i1 = i==1 and (p,p-1) or (p-1,p)
        if cur%i0 != 0: return None  # invalid way
        step = Step(cur/i0, cur, i0,i1, cur*i1/i0)
        steps.append(step)
        cur = step.note1
    if cur != n1: raise Exception("%s != %s", (cur, n1))
    return steps


class Path(object):
    __slots__ = 'n0','n1','steps','way'
    def __init__(self, n0,n1, way):
        self.n0 = n0
        self.n1 = n1
        self.way = ' '.join("%d/%d" % (i==1 and (p,p-1) or (p-1,p)) for (p,i) in way)  # for trace only
        self.steps = getSteps(n0,n1, way)
    def isValid(self):
        return self.steps is not None
    def __str__(self):
        return "path %s -> %s: %s" % (self.n0, self.n1, self.way)
    def getAllNotes(self):
        return (self.n0,) + tuple(s.note1 for s in self.steps)
    def getAllScalas(self):
        return tuple(set(s.scala for s in self.steps))

def getPaths(n0,n1):
    r = Rational(n0,n1)
    for way in getEpimoricWays(r):
        p = Path(n0,n1, way)
        if p.isValid():
            yield p


def formatTable(table):
    widths = [max(len(row[j]) for row in table)  for j in range(len(table[0]))]
    return "\n".join(" ".join(s.center(widths[j])  for (j,s) in enumerate(row))  for row in table)


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
    return formatTable(table)


class Chord(object):
    __slots__ = 'notes','paths', 'scalas','structId','scalaSteps'
    def __init__(self, notes, paths):
        self.notes = notes
        self.paths = paths
        self.init()
    def init(self):
        # define scalas and id
        from collections import defaultdict
        scalas = defaultdict(set)
        for path in self.paths:
            for step in path.steps:
                scalas[step.scala].add(step.i0)
                scalas[step.scala].add(step.i1)
        # scalas
        self.scalas = tuple(sorted(scalas.keys()))
        # structId
        self.structId = (tuple(self.notes),)
        for s in self.scalas:
            self.structId += (s, tuple(sorted(scalas[s])))
        # scalaSteps
        self.scalaSteps = {}
        for s in self.scalas:
            ps = []
            for p in primes:
                if p in scalas[s] and (p-1) in scalas[s]:
                    ps.append(p)
                elif p > max(scalas[s]):
                    break
            self.scalaSteps[s] = tuple(ps)
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
    def getRate(self):
        return (
            len(self.scalas),
            len(self.getAllNotes()),
            reduce(utils.lcm, self.scalas),
            utils.mult(self.scalas),
        )
    def getBestChains(self):
        if len(self.scalas) == 1:
            return [[self]]
        childChains = findBestChains(self.scalas)
        return [[self]+c for c in childChains]

def generateAllPathCombinations(notes):             # 4,5,6
    pairs = tuple(itertools.combinations(notes, 2)) # (4,5), (4,6), (5,6)
    print 'pairs (%d):' % len(pairs), pairs
    paths = [list(getPaths(*p)) for p in pairs]   # paths of (4,5), paths of (4,6), paths of (5,6)
    #for pp in paths: print 'paths', pp[0].n0, pp[0].n1, len(pp), [p.way for p in pp]
    return itertools.product(*paths)        # all interpretations


def findBestChords(notes):
    print "findBestChords", notes
    chords = (Chord(notes, paths) for paths in generateAllPathCombinations(notes))
    chords = utils.findBestItems(chords, lambda c: c.getRate())
    chords = utils.distinct(chords, key= lambda c: c.structId)
    return chords


def findBestChains(notes):
    #print "findBestChains", notes
    chords = findBestChords(notes)
    #print "findBestChains", notes, "->", len(chords)
    
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



def formatChord(chord):
    from collections import defaultdict
    #
    grid = defaultdict(defaultdict)
    for n in chord.notes:
        grid[1][n] = n
    for path in chord.paths:
        for s in path.steps:
            grid[s.scala][s.note0] = s.i0
            grid[s.scala][s.note1] = s.i1
    #
    scalas = sorted(grid.keys())
    columns = sorted(set(j   for row in grid.values()   for j in row.keys()))
    #
    table = []
    table.append([""] + [(j in chord.notes and "." or "") for j in columns])  # columns header
    for i in scalas:
        def cell(j):
            n = grid[i].get(j)
            if n is not None: return str(n)
            if i == 1: return "[%s]" % j
            return ""
        table.append(["(%d)" % i] + [cell(j) for j in columns])
    #
    
    #return formatTable(table)
    widths = [max(len(row[j]) for row in table)  for j in range(len(table[0]))]
    lines = [" ".join(s.center(widths[j])  for (j,s) in enumerate(row))  for row in table]
    
    # draw (p-1)-----(p) lines   !!! ugly hack :)
    for (i,s) in enumerate(scalas):
        line = lines[i+1]
        for p in chord.scalaSteps.get(s, ()):
            for r in range(1, len(line)):
                line = line.replace(`p-1`+(" "*r)+`p`, `p-1`+("-"*r)+`p`)
        lines[i+1] = line
    
    #lines.insert(0, `chord.structId`)
    
    return "\n".join(lines)
    


def formatChain(chain):
    allNotes = sorted(set(note   for chord in chain   for note in chord.getAllNotes()))
    return "\n".join(formatChord(chord, allNotes) for chord in chain)


def test():
    for path in getPaths(9, 5):
        print "=" * 30
        print path.n0, "->", path.n1, "way", path.way
        for s in path.steps: print str(s)
        f = formatPath(path)
        if f:
            print
            print f

def test3():
    from chords import generateChords
    allNotes = utils.take(100, generateChords(noteRange= (3,4)))
    for notes in allNotes:
        print "="*20, notes
        chains = findBestChains(notes)
        for chain in chains:
            for chord in chain:
                #print chord
                print formatChord(chord)
            #print formatChain(chain)
            print

def test4():
    notes = 108,135,162
    notes = 108,135,162,196
    notes =     135,162,160,196
    notes =         162,160,196
    if 0:
        chains = findBestChains(notes)
        for chain in chains:
            for chord in chain:
                #print chord
                print formatChord(chord)
            #print formatChain(chain)
            print
    else:
        chords = findBestChords(notes)
        for chord in chords:
            print formatChord(chord)


"""
findBestChords (162, 160, 196)
pairs (3): ((162, 160), (162, 196), (160, 196))
                                       .   .         .
(1)  [64] [72] [96] [108] [128] [144] 160 162 [168] 196
(24)                              6-------------7
(28)                                            6----7
(32)  2---------3           4----------5
(36)       2----------3
(48)            2-----------------3
(54)                  2--------------------3
(64)  1---------------------2
(72)       1----------------------2
"""


if __name__ == "__main__":
    Rational.__repr__ = Rational.__str__
    test4()
