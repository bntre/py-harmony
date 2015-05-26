
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

def getEpimoricPaths(r):                                # 9/5 ->
    z = getEpimoricZip(r)                               # [    (3,2),       (5,-1)  ]
    groups = [ [(e,k/abs(k))] * abs(k) for (e,k) in z]  # [ [(3,1),(3,1)], [(5,-1)] ]
    for perm in utils.permutations_groups(groups):      # [(3,1),(3,1),(5,-1)], [(3,1),(5,-1),(3,1)],..
        yield perm


def formatPath(r0, r1, path):
    from collections import defaultdict
    from utils       import defaultlist
    #
    grid = defaultdict(defaultdict)
    #
    cur = r0
    for (e,s) in path:
        i0,i1 = (e ** s).getFraction()
        j = cur/i0
        grid[cur][j] = i0
        cur = cur*i1/i0
        grid[cur][j] = i1
    grid[r0][Rational(1)] = r0
    grid[r1][Rational(1)] = r1
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
        h = i in (r0,r1) and ">" or ""  # row header
        table.append([h] + [cell(j) for j in columns])
    #for row in table: print row

    # result
    widths = [max(len(row[j]) for row in table) for j in range(len(table[0]))]
    return "\n".join(" ".join(s.center(widths[j]) for (j,s) in enumerate(row)) for row in table)


def test():
    Rational.__repr__ = Rational.__str__
    #r = Rational(21, 8)
    #r = Rational(9, 5)
    #r = Rational(81, 80)
    r0 = Rational(9)
    r1 = Rational(5)
    r = r0/r1
    print r0, "->", r1, "zip:", getEpimoricZip(r)
    for p in getEpimoricPaths(r):
        print "=" * 30
        print r0, "->", r1, "path", p
        f = formatPath(r0, r1, p)
        if f:
            print
            print f

def test2():
    print Rational.gcd(Rational(3,2), Rational(6,2))

if __name__ == "__main__":
    test()
