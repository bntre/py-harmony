
import itertools
import math    
import colorsys
from collections import defaultdict

import svgwrite
from svgwrite import cm, mm

from utils import defaultlist, primes, factor


def getAllDivisors(n):
    for i in range(1,n+1):
        if n%i == 0:
            yield i

def getHue(index):
    #return math.log(index*2+1, 2) % 1.0
    return (0.6 - math.log(index*2+1, 2)) % 1.0


def draw_grid(name):

    N = 100
    
    width = math.log(N, 2)
    dwg = svgwrite.Drawing(
        filename=name, 
        debug=True
    )
    
    limitItems = defaultdict(list)
    limitCurrent = 0

    def coord(i, j):
        return math.log(i,2)+math.log(j,2), math.log(i,2)
    
    def getLineWidth(p, j):
        k = 1.5/p
        return k / j
    
    def getPointRadius(j):
        return 0.6/j
    
    def getColor(index):
        h = getHue(index)
        col = colorsys.hsv_to_rgb( h, 0.7, 0.9 )
        return "#%02x%02x%02x" % tuple( map( lambda f: int(f*0xFF), col ) )
        
    scale = 100
    def scalePoint(c): return (c[0]+0.5)*scale, (c[1]+0.5)*scale
    
    def line(c0,c1, w, stroke):
        if c1[0] > width: c1 = (width, c1[1])
        limitItems[limitCurrent].append(dwg.line(start=scalePoint(c0), end=scalePoint(c1), stroke='white', stroke_width= w*1.2*scale))
        limitItems[limitCurrent].append(dwg.line(start=scalePoint(c0), end=scalePoint(c1), stroke=stroke, stroke_width= w*scale))
    
    def point(c,r, fill, i):
        limitItems[limitCurrent].append(dwg.circle(center=scalePoint(c), r= r*scale, fill= fill))
        #
        minsize = 0.035
        s = r*1.8 + minsize
        c = (c[0], c[1] + s*0.35)
        #c = (c[0], c[1] + (i%3)*minsize)
        if getPointRadius(i) <= minsize:
            c = (c[0], c[1] + (i%3-1)*minsize)
        limitItems[limitCurrent].append(dwg.text(`i`, scalePoint(c), font_size= s*scale, font_family= "Arial", style="text-anchor:middle;text-align:center"))

        
    
    ns = range(1, N+1)
    ps = list(itertools.takewhile(lambda p: p <= N, primes()))

    limitCurrent = 1
    point(coord(1, 1), getPointRadius(1), getColor(0), 1)

    #for pi,p in enumerate(ps):  # ji limit
    for pi,p in enumerate([2,3,5,7]):  # ji limit
        
        limitCurrent = p
        fillColor = getColor(pi)

        # verticals
        for j in ns:
            if j>1 and max(factor(j))==p:
                c0 = coord(1, j)
                c1 = coord(j, 1)
                line(c0,c1, getLineWidth(p, j), fillColor)

        # horizontals
        for i in ns:
            for j in ps:
                if i==1 or max(factor(i*j))==p:
                    if j<=p and i*(j-1)<=N:
                        c0 = coord(i, j-1)
                        c1 = coord(i, j)
                        line(c0,c1, getLineWidth(p, j*i), fillColor)
        
        # points
        for j in ns:
            if j>1 and max(factor(j))==p:
                for i in getAllDivisors(j):
                    jj = j/i
                    c0 = coord(i, jj)
                    point(c0, getPointRadius(jj*i), fillColor, jj)
                    
        

    for l in sorted(limitItems.keys())[::-1]:
        group = dwg.add(dwg.g(id='limit'+`l`))
        for i in limitItems[l]:
            group.add(i)
    
    dwg.save()
    



def open(fileName):
    import subprocess
    subprocess.Popen([
        r"C:\Documents and Settings\bntr\Local Settings\Application Data\Google\Chrome\Application\chrome.exe",
        #r'--profile-directory="Profile 1"',
        fileName
    ])

def test():
    #open(r"U:\Bntr\+Archive\My\Py\+3rd_side\svgwrite\examples\basic_shapes.svg")

    fileName = 'epimoric_grid.svg'
    #basic_shapes(fileName)
    #draw_test(fileName)
    draw_grid(fileName)
    open(fileName)


def test2():
    print tuple(getAllDivisors(12))
    


if __name__ == "__main__":
    test()
