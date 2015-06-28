
import itertools
from collections import defaultdict

import utils
from rationals import Rational

primes = list(itertools.islice(utils.primes(), 100))




def getStepPair(step):
    """  p  ->  p/(p-1)
        -p  ->  (p-1)/p  """
    return step > 0 and (step, step-1) or (-step-1, -step)

def formatStep(step):
    return "%d/%d" % getStepPair(step)
    
def getSteps(n0, n1):
    #"(6/5) -> [(3/2,1), (5/4,-1)]"
    #"(6/5) -> [(3,1), (5,-1)]"
    "(6/5) -> (3, -5)"
    result = ()
    r = Rational(n1, n0)
    while r != Rational(1):
        p, i = zip(primes, r)[-1]
        a = abs(i)
        s = i//a
        for j in range(a):
            result += (p * s,)
        r /= Rational(p, p-1) ** i
    return result

def getHoleSteps(notes):                            # 4,5,6
    pairs = tuple(itertools.combinations(notes, 2)) # (4,5), (4,6), (5,6)
    #print 'pairs (%d):' % len(pairs), pairs
    #
    result = {}
    for (n0,n1) in pairs:
        steps = getSteps(n0,n1)
        result[(n0,n1)] = tuple(steps)
        result[(n1,n0)] = tuple(-s for s in steps)
    #for k in result.keys(): print k, result[k]
    return result

def getStepsFromNote(steps, note):
    sss = tuple(ss  for (k,ss) in steps.items()  if k[0] == note)       # all steps from the note
    result = tuple(reduce(set.intersection, (set(ss) for ss in sss)))   # get common steps
    result = tuple(s  for s in result  if isPossibleStep(note, s))      # possible steps only
    return result

def isPossibleStep(note, step):
    n0,n1 = getStepPair(step)
    return note % n1 == 0
    
def stepFromNote(note, step):
    n0,n1 = getStepPair(step)
    return note * n0/n1

def removeStep(steps, step):
    l = list(steps)
    l.remove(step)
    return tuple(l)
    

def makeStepFromNote(steps, note, step):
    n = stepFromNote(note, step)
    result = {}
    for (k,ss) in steps.items():
        if k[0] == note:
            result[(n,k[1])] = removeStep(steps[k],  step)
        elif k[1] == note:
            result[(k[0],n)] = removeStep(steps[k], -step)
        else:
            result[k] = ss  # copy
    return result

def removeNoteFromSteps(steps, note):   
    result = {}
    for (k,ss) in steps.items():
        if note not in k:
            result[k] = ss  # copy
    return result
    


class Tree(object):
    __slots__ = 'note','children'
    def __init__(self, note, children= None):
        self.note     = note
        self.children = children or {}  # step -> Tree
    def __str__(self):
        r = `self.note`
        if self.children:
            r += " (%s)" % ", ".join("%s -> %s" % (formatStep(s), t) for (s,t) in self.children.items())
        return r
    def format(self, tab= 0):
        """5 (6/5) 6
             (3/2) 4"""
        nn = `self.note`
        result = nn
        for (i,(s,c)) in enumerate(self.children.items()):
            ss = " (%s) " % formatStep(s)
            tss = ' '*(tab+len(nn)) + ss
            if i != 0: ss = '\n' + tss
            result += ss + c.format(len(tss))
        return result
    def copy(self): 
        import copy
        return copy.deepcopy(self)
    #def getAllNotes(self):
    #    def g(t): return (t.note,) + tuple(n  for c in t.children.values()  for n in g(c))
    #    return tuple(sorted(g(self)))
    def getId(self):
        return getTreeId(self)


def getTreeId(tree):
    "returns a sorted tuple of tree edge pairs"
    edges = []
    def addEdge(n0,n1): edges.append(n0<n1 and (n0,n1) or (n1,n0))
    def g(t):
        for c in t.children.values():
            addEdge(t.note, c.note)
            g(c)
    g(tree)
    return tuple(sorted(edges))
    
def getTreesId(trees):
    return tuple(sorted(
        ((t.note, getTreeId(t)) for t in trees), 
        key= lambda p: p[0]
    ))


class Hole(object):
    __slots__ = 'steps','trees'
    def __init__(self, steps, trees):
        self.steps = steps  # note pair -> tuple of steps
        self.trees = trees  # tuple of trees
    def __str__(self):
        r = "Hole"
        if len(self.trees) == 1:
            r += "\n tree: " + self.trees[0].format()
        else:
            r += "\n trees: \n" + "\n".join("  "+t.format(2) for t in self.trees)
        if self.steps:
            r += "\n steps:\n" + "\n".join("  %s: %s" % (k, " ".join(formatStep(s) for s in ss)) for (k,ss) in self.steps.items())
        return r
    def copy(self):
        import copy
        return copy.deepcopy(self)



def makeStep(hole, note, step):
    n = stepFromNote(note, step)
    #
    steps = makeStepFromNote(hole.steps, note, step)
    for k in tuple(steps.keys()):
        if not steps[k]:
            del steps[k]
    #
    def getNewTree(t):
        if t.note != note:
            return t.copy()
        else:
            return Tree(n, {-step: t})
    trees = [getNewTree(t) for t in hole.trees]
    tt = [t  for t in trees  if t.note == n]
    if len(tt) > 1:
        for t in tt[1:]:
            tt[0].children.update(t.children)
            trees.remove(t)
    #
    return Hole(steps, tuple(trees))


def distinctById(trees):
    return utils.distinct(trees, key= lambda t: t.getId())
    

def iterTrees(hole, holesTried= None):
    #
    if len(hole.trees) == 0: raise Exception('Invalid Hole')
    if len(hole.trees) == 1:
        yield hole.trees[0]  # solution tree found
        return
    #
    # optimization
    if holesTried == None: holesTried = set()
    holeId = getTreesId(hole.trees)
    if holeId in holesTried: return
    holesTried.add(holeId)
    #
    stepsDone = False
    notes = tuple(t.note for t in hole.trees)
    for note in notes:
        steps = getStepsFromNote(hole.steps, note)
        if steps:
            #print 'steps:', note, [formatStep(s) for s in steps]
            for step in steps:
                h = makeStep(hole, note, step)
                for t in iterTrees(h, holesTried):
                    yield t
            stepsDone = True
    if stepsDone: return
    #
    # no steps available - probably diamond structure
    treeCut, newHole = cutTree(hole)
    #print 'tree cut'
    #print treeCut.format()
    #print 'new hole', newHole
    #for t in iterTrees(newHole):
    for t in distinctById(iterTrees(newHole)):
        for tt in joinTrees(t, treeCut):
            yield tt


def cutTree(hole):
    tree = max(hole.trees, key= lambda t: t.note)
    trees = tuple(t.copy()  for t in hole.trees  if t != tree)
    steps = removeNoteFromSteps(hole.steps, tree.note)
    return tree, Hole(steps, trees)



def joinTrees(tree, treeCut, steps= None):
    if steps == None:
        steps = getSteps(tree.note, treeCut.note)

    #print 'joinTrees', tree.note, '<-', treeCut.note, steps
    #print tree.format()
    #print treeCut.format()
    
    childFound = False
    for (s,child) in tree.children.items():
        if s in steps:
            ss = removeStep(steps, s)
            for t in joinTrees(child, treeCut, ss):
                tt = tree.copy()
                tt.children[s] = t  # replace the child
                yield tt
            childFound = True
    #
    if not childFound:
        for w in utils.distinct(itertools.permutations(steps)):
            child = treeCut.copy()
            for s in w[:0:-1]:
                child = Tree(stepFromNote(child.note, -s), {s: child})
            tt = tree.copy()
            tt.children[w[0]] = child
            yield tt



def findTrees(notes):
    hole = Hole(
        getHoleSteps(notes), 
        tuple(Tree(n) for n in notes)
    )
    print hole
    print '-'*20
    #
    for t in distinctById(iterTrees(hole)):
        print t.format()
        print formatTree(t, notes)
        print '-'*5
    


def formatTree(tree, notes):
    grid  = defaultdict(lambda: defaultdict(str))
    lines = defaultdict(list)  # list of pairs

    for n in notes:
        grid[0][n] = '.'
        grid[1][n] = `n`
    
    def fillGrid(t):
        for (s,child) in t.children.items():
            n0,n1 = getStepPair(s)
            scala = t.note / n1
            note1 = t.note
            note0 = t.note * n0/n1
            grid[scala][note1] = `n1`
            grid[scala][note0] = `n0`
            lines[scala].append(tuple(sorted([note0,note1])))
            fillGrid(child)
    fillGrid(tree)
    
    scalas  =       sorted(grid.keys())
    columns = [0] + sorted(set(j  for row in grid.values()  for j in row.keys()))

    # headers
    for s in scalas:
        if s != 0:
            grid[s][0] = "(%d)" % s
    for c in columns:
        if c != 0 and not grid[1][c]:
            grid[1][c] = "[%s]" % c
    
    widths = {}
    for c in columns:
        widths[c] = max(len(grid[s][c])+1 for s in scalas)

    def cell(s,c):
        n = grid[s][c]
        w = widths[c]
        t0,t1 = ' ',' ' # tabulators
        for l in lines[s]:
            if   l[0] == c: t1 = '-'
            elif l[1] == c: t0 = '-'
            elif l[0] < c < l[1]: t0,t1 = '-','-'
        a0 = (w - len(n))/2
        a1 = (w - len(n)) - a0
        return t0*a0 + n + t1*a1
    
    return "\n".join("".join(cell(s,c) for c in columns) for s in scalas)


def test():
    #print [formatCodePair(code) for code in getEpimoricWay(15, 8)]
    notes = 4,5,6
    notes = 10,12,15
    notes = 8,12,15,18
    notes = 108,135,    160,192
    notes = 81,80
    notes = 64,81,96
    notes = 54,64,243
    notes = 3,5,7,9
    notes = 4,5,6,18
    notes = 10,12,15,18
    notes = 20,25,30,36
    notes = 25,30,36,45
    notes = 40,48,60,75
    notes = 80,100,125,144
    notes =  36, 45, 54,     64
    notes = 2,3,4,6
    notes = 108,135,162,    192
    notes = 108,135,162,160,192
    findTrees(notes)

if __name__ == "__main__":
    Rational.__repr__ = Rational.__str__
    test()

