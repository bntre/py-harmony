
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
    print 'pairs (%d):' % len(pairs), pairs
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


def makeStepFromNote(steps, note, step):
    def remove(ss, s):
        l = list(ss)
        l.remove(s)
        return tuple(l)
    for (k,ss) in steps.items():
        if k[0] == note:
            steps[k] = remove(steps[k], step)
        elif k[1] == note:
            steps[k] = remove(steps[k], -step)


class Tree(object):
    __slots__ = 'note','children'
    def __init__(self, note):
        self.note     = note
        self.children = []  # [(step,Tree)]
    def __str__(self):
        r = `self.note`
        if self.children:
            r += " (%s)" % ",".join("%s -> %s" % (formatStep(s), t) for (s,t) in self.children)
        return r

def growTree(tree, step):
    child = Tree(t.note)
    child.children = tree.children
    tree.children = (child,)
    tree.note = stepFromNote(tree.note, step)


class Hole(object):
    __slots__ = 'steps','trees'
    def __init__(self, steps, trees):
        self.steps = steps
        self.trees = trees
    def __str__(self):
        r = "Hole trees:\n" + "\n".join(" %s" % t for t in self.trees)
        r += "\n" + "steps:\n" + "\n".join(" %s: %s" % (k, " ".join(formatStep(s) for s in ss)) for (k,ss) in self.steps.items())
        return r
    def copy(self):
        import copy
        return copy.deepcopy(self)


def process(hole):
    print 'process', hole
    notes = tuple(t.note for t in hole.trees)
    for note in notes:
        steps = getStepsFromNote(hole.steps, note)
        print 'steps:', note, [formatStep(s) for s in steps]
        for step in steps:
            h = hole.copy()
            # update steps
            makeStepFromNote(h.steps, note, step)
            # update trees
            for t in h.trees:
                if t.note == note:
                    growTree(t, step)
                    break




def findTrees(notes):
    steps = getHoleSteps(notes)
    trees = tuple(Tree(n) for n in notes)
    hole = Hole(steps, trees)
    process(hole)
    


def test():
    #print [formatCodePair(code) for code in getEpimoricWay(15, 8)]
    notes = 4,5,6
    findTrees(notes)

if __name__ == "__main__":
    Rational.__repr__ = Rational.__str__
    test()

