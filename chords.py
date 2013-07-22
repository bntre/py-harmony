
import math
import utils

def coprimes(*numbers):
    for p in utils.primes():
        if all(n%p == 0 for n in numbers): return False
        if all(n/p == 0 for n in numbers): return True  # stop searching


def generateChords(noteRange= (3, 4), maxWidth= 1.999):
    for last in utils.integers(1):  # last harmonic present in a chord
        first = int(math.ceil(last/maxWidth))
        harms = range(first, last)  # harmonics to choose
        if len(harms) == 0: continue
        for count in range(noteRange[0]-1, noteRange[1]):  # (3, 4) -> 2..3
            if len(harms) < count: continue
            for c in utils.combinations(harms, count):
                chord = c + (last,)
                if coprimes(*chord):
                    yield chord



def getHarmonicDistance(chord, weights= ()):
    "chord as a list of integers, weights - floats"
    from rationals import Rational
    import harmonicity 
    
    #print chord, weights
    if not weights: weights = (1.0,) * len(chord)
    
    variations = list( utils.variations(len(chord)) )
    distance = 0.0
    for var in variations:
        ns = [ n for (n,b) in zip(chord, var) if b ]
        ws = [ w for (w,b) in zip(weights, var) if b ]
        if len(ns) >= 2:
            m = reduce(utils.lcm, ns)
            r = Rational(m)
            d = harmonicity.simple(5)(r)
            dw = d * utils.mult(ws)
            #print "  ", ns, m, `r`, d #, dw
            distance += dw
    return distance



def test_generate():
    from rationals import Rational
    chords = utils.take(1000, generateChords((3,3)));
    chords = [(c, getHarmonicDistance(c)) for c in chords ]
    chords.sort(key= lambda (c,d): d)
    
    for (i,(c,d)) in enumerate(chords[:50]):
        chord = map(Rational, c)
        for j in range(len(chord))[::-1]: chord[j] /= chord[0]  # normalize
        # print
        print "%03d." % (i+1), c,
        for r in chord:
            print r.getFraction(0),
            #print r.getSonant(),
        print d
    
def test_distance():
    print getHarmonicDistance([10, 12, 15], (1.0, 0.3, 1.0))


if __name__ == "__main__":
    test_generate()
    #test_distance()



