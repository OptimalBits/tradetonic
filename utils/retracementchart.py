
import svg
from rect import *
from path import Path
from text import *
from pygraph import *
from retracement import *
from line import *

def bars( values ):
    from decimal import Decimal
    from copy import copy
    g = group.Group()
    
    r = rect.Rect()
    r.x = 0
    r.y = 0
    r.width = 10
    r.height = 10
    r.rx = 0

    x, y = zip(*values)
        
    maxx, minx = ( max(x), min(x) )
    maxy, miny = ( max(y), min(y) )
        
    width = maxx - minx
    height = ( maxy - miny ) * 10
    
    T = 0
    for t in values:
        level = Decimal(str(t[0])).quantize(Decimal('1.00'))
    
        label = text.Text(str(level) )
        label.translate( 0, T + 10)
        g.append( label )
        
        probability = Decimal(str(t[1])).quantize(Decimal('1.00'))

        label = text.Text(str(probability) )
        label.translate( t[1] * 10 + 80, T + 5)
        
        g.append( label )
        
        bar = copy(r)
        bar.translate( 70, T )
        bar.scale( t[1], 1 )
        g.append( bar )
        T = T + 20
   
    p = Paint ()
    p.fill ="red"
    p.stroke = "black"
    p.stroke_width = 2
        
    axisx = AxisX ( (70, T), height * 1.10, 2*10, p )
    axisy = AxisY ( (70, T), len(values) * 20, 20, p )
    g.append( axisx )
    g.append( axisy )
    return g
    
    
def plot( values ):
    pass
    

class RetracementLevelsChart(svg.Svg):      
       def __init__ ( self, title, desc, values ):
        svg.Svg.__init__(self)
        
        self.setXmlSpace (True)
        self.setId ("Retracement Levels")
        self.setXmlLang ("english")
        
        self.width = 1000
        self.height = 1000
                
        # Frame
        frame = group.Group()
        r = rect.Rect()
        r.x = 0
        r.y = 0
        r.width = 400
        r.height = 450
        r.rx = 20
        r.stroke = "grey"
        r.stroke_width = 2
        r.fill = "none"
        frame.append( r )
        frame.translate ( 50, 50 )
        self.append( frame )
 
        # Chart       
        chart = group.Group()        
        chart.translate( 50, 50 )
        frame.append( chart )
        
        # Create the bar template
        r = rect.Rect()
        r.x = 0
        r.y = 0
        r.width = 10
        r.height = 10
        r.rx = 0
       
        title_text = text.Text( title )
        title_text.translate ( 50, -30 )
        chart.append( title_text )
        
        desc_text = text.Text( desc )
        desc_text.font_size = "80%"
        desc_text.translate(105, -15 )
        chart.append( desc_text )
        
        chart.append( bars( values ) )
 
        #grid = Grid( b.viewport, 25, 1, p )
        #self.append(grid)
        
        
class FibonacciChart(svg.Svg):      
       def __init__ ( self, title, desc, values, levels ):
        svg.Svg.__init__(self)
        
        self.setXmlSpace (True)
        self.setId ("Retracement Levels")
        self.setXmlLang ("english")
        
        width = 400
        height = 400
        
    #    self.width = 1000
    #    self.height = 1000
                
        # Frame
        frame = group.Group()
        r = rect.Rect()
        r.x = 0
        r.y = 0
        r.width = width * 1.2
        r.height = height * 1.2
        r.rx = 20
        r.stroke = "grey"
        r.stroke_width = 2
        r.fill = "none"
        frame.append( r )
        frame.translate ( 50, 50 )
        self.append( frame )
 
        # Chart       
        chart = group.Group()        
        chart.translate( 50, 50 )
        frame.append( chart )
        
        # Plot
        p = Paint ()
        p.fill ="red"
        p.stroke = "black"
        p.stroke_width = 3

        
        plot_group = group.Group()
        plot = Plot( values, p )
    
        x, y = zip(*values)
        
        minx = min(x)
        miny = min(y)
       
        plot_width = max(x) - minx
        plot_height = max(y) - miny
        
        print miny
        print plot_height

        for l in levels:
            fibo_line = Line()
            fibo_line.x1 = 0
            fibo_line.x2 = plot_width
            fibo_line.y1 = l[0]
            fibo_line.y2 = l[0]
            plot.append( fibo_line )
        

        scalex = float(width) / float(plot_width)
        scaley = float(height) / float(plot_height)
        
        plot_group.scale( scalex, scaley )
        plot.translate( 0, -miny )
        
        plot_group.append(plot)

        chart.append( plot_group )   
    
        title_text = text.Text( title )
        title_text.translate ( 50, -30 )
        chart.append( title_text )
        
        desc_text = text.Text( desc )
        desc_text.font_size = "80%"
        desc_text.translate(105, -15 )
        chart.append( desc_text )
        
    
        #chart.append( bars( values ) )
 
        #grid = Grid( b.viewport, 25, 1, p )
        #self.append(grid)
        
input = open("goldprice.txt", "rb")
lines = input.readlines()
input.close()

quotes = []
plot = []
i = 0

#lines.reverse()

for l in lines:
#	date  = l[:10]
	value = l[11:-2]
	quotes.append( float(value) )
	plot.append( (i,float(value)) )	
	i = i + 1

t1 = 1360.03
b  = 1342.53
t2 = 1353.11
rl = get_retracements( t1, b, t2 )

b = RetracementLevelsChart( "Frequency of LONG reversals (%)", "Gold Bladusir", rl )

#b = FibonacciChart( "Fibonacci levels", "Gold Bladusir", plot[0:1000], rl )

f = open ( 'test.svg', 'wb' )
f.write ( svg.svgdoc(b) )
f.close()

