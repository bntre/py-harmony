
import itertools

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
    r = Rational(n0, n1)
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
        result[(n1,n0)] = tuple(steps)
        result[(n0,n1)] = tuple(-s for s in steps)
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


def makeStepFromNote(steps, note, step):
    def remove(ss, s):
        l = list(ss)
        l.remove(s)
        return tuple(l)
    n = stepFromNote(note, step)
    result = {}
    for (k,ss) in steps.items():
        if k[0] == note:
            result[(n,k[1])] = remove(steps[k],  step)
        elif k[1] == note:
            result[(k[0],n)] = remove(steps[k], -step)
        else:
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
        "returns a sorted tuple of tree edge pairs"
        edges = []
        def addEdge(n0,n1): edges.append(n0<n1 and (n0,n1) or (n1,n0))
        def g(t):
            for c in t.children.values():
                addEdge(t.note, c.note)
                g(c)
        g(self)
        return tuple(sorted(edges))



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



def iterHoles(hole):
    #
    #
    if len(hole.trees) == 0: raise Exception('Invalid Hole')
    if len(hole.trees) == 1:
        yield hole
        return
    stepsDone = False
    notes = tuple(t.note for t in hole.trees)
    for note in notes:
        steps = getStepsFromNote(hole.steps, note)
        if steps:
            #print 'steps:', note, [formatStep(s) for s in steps]
            for step in steps:
                h = makeStep(hole, note, step)
                for hh in iterHoles(h):
                    yield hh
            stepsDone = True
    if not stepsDone:
        yield hole  # no steps available
            


def findTrees(notes):
    hole = Hole(
        getHoleSteps(notes), 
        tuple(Tree(n) for n in notes)
    )
    print hole
    print
    #
    holes = list(iterHoles(hole))
    trees = [h.trees[0]  for h in holes  if len(h.trees) == 1]
    holes = [h           for h in holes  if len(h.trees) != 1]
    trees = utils.distinct(trees, lambda t: t.getId())
    for t in trees:
        #print t
        print t.format()
    for h in holes:
        print h
    
    


def test():
    #print [formatCodePair(code) for code in getEpimoricWay(15, 8)]
    notes = 4,5,6
    notes = 10,12,15
    notes = 8,12,15,18
    notes = 108,135,162,160,196
    notes = 108,135,    160,196
    notes = 36,45,54,64
    findTrees(notes)

if __name__ == "__main__":
    Rational.__repr__ = Rational.__str__
    test()

