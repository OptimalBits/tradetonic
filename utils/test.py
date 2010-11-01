
from rect import *
from path import Path
from svg import *
from text import *
from pygraph import *
from retracement import *

svg = Svg ()

svg.setXmlSpace (True)
svg.id =  "Retracement Levels"
svg.setXmlLang ("english")

svg.width = 1000
svg.height = 1000

r = Rect ()
r.x = 10
r.y = 20
r.width = 100
r.height = 200
r.rx = 20

r.fill ="red"
r.stroke = "black"
r.translate ( 500,400 )

paint = Paint ()
paint.fill ="red"
paint.stroke = "black"
paint.stroke_width = 2

p = Path ()

p.moveto ( ((0,0),(150, 200), (200,300)) ) 
p.curveto ( (50,50, 100, 34, 203.3,124) )
p.stroke = "blue"

a = text.Text ( "rewrewewr" )

#svg.extend([r, p, a])
#print svgdoc ( svg )

plot = Plot (  [( 0, 12), (2, 654), (4, 234), (10, 100),( 15, 123), (20, 98), (25, 38), (30, 178), (35, 189)], paint )


l = DateLabels ( datetime(2009,4,3, 9), datetime(2009,4,3, 17), (timedelta(hours=1), 30, 30), '%H')

l.stroke = "black"
#print l

viewport = Viewport(0,0,500,500)

#chart = Chart ( viewport, axis, True )

t1 = 1360.03
b  = 1342.53
t2 = 1353.11
rl = get_retracements( t1, b, t2 )

b = RetracementLevelsChart( rl )

#b = Bars( r, rl, True )

#chart.append( b )

#b.translate(100,500)
svg.append(b)
#r.translate(100,200)
#svg.append( r )

#svg.append(chart)
#svg.append(l)
#print svg

f = open ( 'test.svg', 'wb' )
f.write ( svgdoc(svg) )
f.close()


