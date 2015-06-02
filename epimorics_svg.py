
import svgwrite
from svgwrite import cm, mm


def basic_shapes(name):
    dwg = svgwrite.Drawing(filename=name, debug=True)
    
    hlines = dwg.add(dwg.g(id='hlines', stroke='green'))
    for y in range(20):
        hlines.add(dwg.line(start=(2*cm, (2+y)*cm), end=(18*cm, (2+y)*cm)))
    
    vlines = dwg.add(dwg.g(id='vline', stroke='blue'))
    for x in range(17):
        vlines.add(dwg.line(start=((2+x)*cm, 2*cm), end=((2+x)*cm, 21*cm)))
        
    shapes = dwg.add(dwg.g(id='shapes', fill='red'))

    # set presentation attributes at object creation as SVG-Attributes
    shapes.add(dwg.circle(center=(15*cm, 8*cm), r='2.5cm', stroke='blue',
                          stroke_width=3))

    # override the 'fill' attribute of the parent group 'shapes'
    shapes.add(dwg.rect(insert=(5*cm, 5*cm), size=(45*mm, 45*mm),
                        fill='blue', stroke='red', stroke_width=3))

    # or set presentation attributes by helper functions of the Presentation-Mixin
    ellipse = shapes.add(dwg.ellipse(center=(10*cm, 15*cm), r=('5cm', '10mm')))
    ellipse.fill('green', opacity=0.5).stroke('black', width=5).dasharray([20, 20])
    
    dwg.save()


def draw_test(name):

    dwg = svgwrite.Drawing(filename=name, debug=True, viewBox=('0 0 10 10'))
    
    group = dwg.add(dwg.g(id='group1'))
    for i in range(10):
        group.add(dwg.line(
            start=(2+i*3, 2), 
            end=  (2+i*3, 5), 
            stroke= "#808000",
            stroke_width= 0.2
        ))
        group.add(dwg.circle(
            center=(2+i*3, 2), 
            r= 0.5, 
            fill= "#008000"
        ))
        group.add(dwg.text(
            "AA", 
            (2+i*3, 2),
            font_size= 2,
            font_family= "Arial",
            style="text-anchor:middle;text-align:center",
        ))

    dwg.save()


def draw_grid(name):

    import math

    dwg = svgwrite.Drawing(filename=name, debug=True, viewBox=('-0.2 -0.2 4 4'))
    
    items = []
    
    def point(c,r, fill, i):
        items.insert(0, dwg.circle(center=c, r= r, fill= fill))
        r = r*1.8
        c = (c[0], c[1]+r*0.35)
        items.insert(1, dwg.text(`i`, c, font_size= r, font_family= "Arial", style="text-anchor:middle;text-align:center"))
    
    def line(c0,c1, w, stroke):
        items.insert(0, dwg.line(start=c0, end=c1, stroke='white', stroke_width= w*1.1))
        items.insert(1, dwg.line(start=c0, end=c1, stroke=stroke, stroke_width= w))
    

    point((0, 0), 0.3/1, '#AAAAAA', 1)
    
    for p in (2, 3, 5, 7):
        c = (math.log(p, 2), 0)
        point(c, 0.3/p, '#AAAAAA', p)
        
        c0 = (math.log(p-1, 2), 0)
        line(c0,c, 0.4/p, '#AAAAAA')
        
        
    group = dwg.add(dwg.g(id='g1'))
    for i in items:
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


if __name__ == "__main__":
    test()
