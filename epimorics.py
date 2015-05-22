
import itertools

import utils
from rationals import Rational

def getEpimoricZip(r):
    "(6/5) -> [(3,1), (5,-1)]   == (3/2)^1 * (5/4)^-1"
    result = []
    while r != Rational(1):
        p, i = zip(utils.primes(), r)[-1]
        result.insert(0, (p, i))
        r /= Rational(p, p-1) ** i
    return result



def getEpimoricPaths(r):                                # 9/5 ->
    z = getEpimoricZip(r)                               # [    (3,2),       (5,-1)  ]
    groups = [ [(p,k/abs(k))] * abs(k) for (p,k) in z]  # [ [(3,1),(3,1)], [(5,-1)] ]
    for perm in utils.permutations_groups(groups):      # [(3,1),(3,1),(5,-1)], [(3,1),(5,-1),(3,1)],..
        yield perm


def formatPath(r, path):
    from collections import defaultdict
    from utils       import defaultlist
    #
    grid = defaultdict(defaultlist)
    (n,d) = r.getFraction()
    #
    cur = n
    for (p,s) in path:
        (i0,i1) = s == 1 and (p,p-1) or (p-1,p)
        if cur/i0*i0 != cur: return None # exception?
        j = cur/i0
        grid[cur][j] = i0
        cur = cur*i1/i0
        grid[cur][j] = i1
    #
    def pad(s, l): return "%%%ds" % l % s
    le = max(2, len(`max(grid.keys())`))
    def header(i, cs):
        if i in (n,d): return ">%s" % pad(" %d " % i, le+2)
        if cs[1] != 0: return " %s" % pad(" %d " % i, le+2)
        else:          return " %s" % pad("[%d]" % i, le+2)
    def line(i, cs):
        for (j,c) in enumerate(cs):
            if   j == 0: continue
            elif j == 1: yield header(i, cs)
            else:        yield pad(c or "", 2)
    lines = []
    if 1:
        w = max(len(v) for v in grid.values())
        if w > 40: return None
        def h(j): return (j == 1 and "  %s " or "%s") % pad(j, 2)
        lines.append("".join(h(j) for j in range(w)[1:]))
        lines.append("")
    for i in sorted(grid.keys())[::-1]:
        lines.append("".join(line(i, grid[i])))
        #lines.append(`grid[i][1:]`)
    return "\n".join(lines)
    

def test():
    #r = Rational(21, 8)
    #r = Rational(9, 5)
    r = Rational(81, 80)
    print "getEpimoricZip", getEpimoricZip(r)
    for p in getEpimoricPaths(r):
        print "=" * 20
        print "path", p
        f = formatPath(r, p)
        if f:
            print
            print f
        


if __name__ == "__main__":
    test()
