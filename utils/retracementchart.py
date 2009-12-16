
import svg
from rect import *
from path import Path
from text import *
from pygraph import *
from retracement import *
from line import *
from decimal import Decimal

NUM_DAYS = 40

def bars( values ):
    
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
        label.translate( t[1] * 10 + 80, T + r.width / 2)
        
        g.append( label )
        
        bar = copy(r)
        bar.translate( 70, T - r.width / 2)
        bar.scale( t[1], 1 )
        g.append( bar )
        T = T + 20
   
    p = Paint ()
    p.stroke = "black"
    p.stroke_width = 1
        
    axisx = AxisX ( (70, T), height * 1.10, 2*10, p )
    axisy = AxisY ( (70, T), len(values) * 20, 20, p )
    g.append( axisx )
    g.append( axisy )
    
    #grid = Grid( b.viewport, 25, 1, p )
    
    #g.append(grid)
    
    return g
    

class RetracementLevelsChart(svg.Svg):      
       def __init__ ( self, id, title, desc, values ):
        svg.Svg.__init__(self)
        
        self.setXmlSpace (True)
        self.setId (id)
        self.setXmlLang ("english")
        
      #  self.width = 1000
      #  self.height = 1000
        
        width = 320
        height = 300
                
        # Frame
        frame = group.Group()
        frame.setId("feo")
        r = rect.Rect()
        r.x = 0
        r.y = 0
        r.width = width * 1.3
        r.height = height * 1.3
        r.rx = 20
        r.stroke = "grey"
        r.stroke_width = 1
        r.fill = "none"
        frame.append( r )
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
         
class FibonacciChart(svg.Svg):      
       def __init__ ( self, title, desc, values, levels, resolution = 1 ):
        svg.Svg.__init__(self)
        
        self.setXmlSpace (True)
#        self.setId (id)
        self.setXmlLang ("english")
        
        width = 320
        height = 300
                
        # Frame
        frame = group.Group()
        r = rect.Rect()
        r.x = 0
        r.y = 0
        r.width = width * 1.3
        r.height = height * 1.3
        r.rx = 20
        r.stroke = "grey"
        r.stroke_width = 1
        r.fill = "none"
        frame.append( r )
        self.append( frame )
 
        # Chart       
        chart = group.Group()        
        chart.translate( 50, 50 )
        frame.append( chart )
        
        # Plot
        p = Paint ()
        p.stroke = "black"
        p.stroke_width = 1
        
        import datetime
        today = datetime.date.today()
        one_year_ago = today - datetime.timedelta( days = NUM_DAYS*resolution )
        
        vavlues = values.samplePrices( resolution )
        prices = values.getClosePrices(one_year_ago, today)
        min_price = min(prices)
        max_price = max(prices)
        
        print prices[-1]
        
        scaley = height / ( max_price - min_price )
        scalex = float(width) / float(len(prices))
        
        v = [ (i*scalex, ((prices[i]-min_price)*scaley)-height ) for i in range(len(prices))]
        
        
        plot = Plot( v, p )

        toggle = True

        prob = 0
        xpos = 10
        startColor = (0,255,0)
        endColor = (255, 0, 0)
        for l in levels:
            if l[0] > 0:
                prob += l[1]
                
                if l[0] > prices[-1]:
                    continue
                    
                if prob > 5 and prob < 99:
                    fibo_line = Line()
                    fibo_line.x1 = 0
                    fibo_line.x2 = len(prices)*scalex
                    fibo_line.y1 = ((l[0]-float(min_price))*float(scaley))-height
                    fibo_line.y2 = ((l[0]-float(min_price))*float(scaley))-height
                    fibo_line.stroke = interpColor( startColor, endColor, prob )
                    fibo_line.stroke_width = "0.8"
                    
                    plot.append( fibo_line )
                    
                    fprob = Decimal(str(prob)).quantize(Decimal("1.0"))
                    fibo_prob = text.Text( str(fprob) + "%")     
                    fibo_prob.font_size = "50%"
                    fibo_prob.font_family= "Verdana"
                    fibo_prob.stroke = fibo_line.stroke
                    fibo_prob.stroke_width = "0.5"                         
                    
                    ypos = fibo_line.y1 * 0.99
                    
                    fibo_prob.scale(1,-1)
                    plot.append( Label(fibo_prob,(xpos,ypos),0) )
                    
                    xpos += 30
        

        
        plot.scale( 1, -1)
     

        chart.append( plot )   
    
        title_text = text.Text( title )
        title_text.translate ( 50, -30 )
        chart.append( title_text )
        
        desc_text = text.Text( desc )
        desc_text.font_size = "80%"
        desc_text.translate(105, -15 )
        chart.append( desc_text )
        
        # Generate X Axis
        month_strings = generateMonthlyStrings( one_year_ago, today )
        
        if len(month_strings) > 1:
            date_tick = width / (len( month_strings ) - 1)
        else:
            date_tick = width
        
        axisx = AxisX ( (0, height), width, date_tick, p )
        
        coords = [ -15, 27 ]
        for label in month_strings:
            label.font_size = "75%"
            l = Label(label, coords, -35 )
            axisx.append(l)
            coords[0] += date_tick
        chart.append( axisx )
        
        # Generate Y Axis
        NUM_TICKS = 7
        price_len = float(max_price - min_price)

        price_tick = height / NUM_TICKS
        price_inc = price_len / NUM_TICKS
        
        #axisy = AxisY ( (0, height), height, price_tick, p )
        
        axisy = group.Group()
        
        y_line = line.Line()
        
        y_line.x1 = 0
        y_line.y1 = height
        y_line.x2 = 0
        y_line.y2 = 0
        y_line.stroke = "green"
        y_line.stroke_width = 1
        
        axisy.append(y_line)
        
        coords = [-40, height]
        
        price_tick = Decimal(str(price_tick)).quantize(Decimal('1.0'))
        price_tick = float(price_tick)

        price_inc = Decimal(str(price_inc)).quantize(Decimal('1.0'))

        p = min_price
        for r in range(0,NUM_TICKS+1 ):
            d = Decimal(p).quantize(Decimal('1.00'))
        
            t = text.Text(str(d))
            t.font_size = "75%"
            l = Label( t, coords, 0 )
            axisy.append(l)
            coords[1] -= price_tick
            p += price_inc
        
        chart.append( axisy )
 
        p = Paint ()
        p.stroke = "black"
        p.stroke_width = 0.2
        p.stroke_dasharray = "3"
        
        grid = Grid( Viewport(0,0,width,height), date_tick, price_tick, p )
        
        chart.append(grid)
       

def interpColor( startColor, endColor, prob ):
    t = prob / 100.0
    a = startColor[0] * ( 1 - t ) + endColor[0] * t
    b = startColor[1] * ( 1 - t ) + endColor[1] * t
    c = startColor[2] * ( 1 - t ) + endColor[2] * t
    
    return "#%02x%02x%02x" % (a,b,c)
    
 




