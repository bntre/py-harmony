
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


def test():
    from rationals import Rational
    for (i,c) in enumerate(generateChords()):
        chord = map(Rational, c)
        for j in range(len(chord))[::-1]: chord[j] /= chord[0]  # normalize
        # print
        print i+1,
        for r in chord:
            print r.getFraction(0),
            #print r.getSonant(),
        print
        if i+1 >= 1000: break
    

if __name__ == "__main__":
    test()



