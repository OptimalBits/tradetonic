
import svg
from rect import *
from path import Path
from text import *
from pygraph import *
from retracement import *
from line import *
from decimal import Decimal

from gradient import *
from pychart2 import *

NUM_DAYS = 180

class RetracementLevelsChart(svg.Svg):      
       def __init__ ( self, id, title, desc, values ):
        svg.Svg.__init__(self)
        
        self.id = id
        self.setXmlSpace (True)
        self.setXmlLang ("english")
        
        width = 440
        height = 380
        
        layoutMgr = LayoutMgr( width, height )

        layoutMgr.addLayout('plot', 0.1, 0.2, 0.8, 0.6 )
        layoutMgr.addLayout('title', 0.0, 0.0, 1.0, 0.2 )
        layoutMgr.addLayout('xlabel', 0.0, 0.1, 0.1, 0.8)

        layoutMgr.addLayout('ylabel', 0.1, 0.8, 0.8, 0.2)
        
        # Add gradient
        plotGradient = LinearGradient()
        plotGradient.id = "plotGradient"
        plotGradient.x2 = 0
        plotGradient.y2 = 1

        plotGradient.append( GradientStop( offset=0.0, stop_color="#889") ) 
        plotGradient.append( GradientStop( offset=0.5, stop_color="#CCE") )
        plotGradient.append( GradientStop( offset=1.0, stop_color="#889") )
        self.append( plotGradient )
             
        barsPaint = Paint()
        barsPaint.fill = plotGradient.getURI()
        barsPaint.stroke = "gray"
 
        # Chart       
        chart = BarsChart( values, barsPaint, layoutMgr )
        
        chart.title = title
        chart.subtitle = desc
        
        chart.render( self, barsPaint )

        
         
class FibonacciChart(svg.Svg):      
       def __init__ ( self, title, desc, values, levels, resolution = 1 ):
        svg.Svg.__init__(self)
        
        self.setXmlSpace (True)
#        self.setId (id)
        self.setXmlLang ("english")
        
        width = 440
        height = 380
        
        layoutMgr = LayoutMgr( width, height )

        layoutMgr.addLayout('plot', 0.1, 0.2, 0.8, 0.6 )
        layoutMgr.addLayout('title', 0.0, 0.0, 1.0, 0.2 )
        layoutMgr.addLayout('xlabel', 0.0, 0.1, 0.1, 0.8)

        layoutMgr.addLayout('ylabel', 0.1, 0.8, 0.8, 0.2)
        
        # Add gradient
        plotGradient = LinearGradient()
        plotGradient.id = "plotGradient"
        plotGradient.x2 = 0
        plotGradient.y2 = 1

        plotGradient.append( GradientStop( offset=0.0, stop_color="#889") ) 
        plotGradient.append( GradientStop( offset=0.5, stop_color="#CCE", stop_opacity=0.5) )
        self.append( plotGradient )

        # Chart
        import datetime
        today = datetime.date.today()
        start_date = today - datetime.timedelta( days = NUM_DAYS*resolution )
        
        tsc = TimeSeriesChart( start_date, today, layoutMgr )
       
        # Plot
        p = Paint ()
        p.stroke = "blue"
        p.fill = plotGradient.getURI()
        
        values = values.samplePrices( resolution )
        prices = values.getClosePrices(start_date, today)
        
        tsc.addPlot( prices, p )
        
        p = Paint ()
        p.stroke = "gray"
        p.fill = "none"
        p.stroke_width = 0.5
        tsc.render( self, p )
       
        """
        toggle = True

        prob = 0
        xpos = 10
        startColor = (0,255,0)
        endColor = (255, 0, 0)
        for l in levels:
            if l[0] > 0:
                prob += l[1]
                
              #  if l[0] > prices[-1]:
               #     continue
                    
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
                    fprice = Decimal(str(l[0])).quantize(Decimal('1.0'))
                    fibo_prob = text.Text( str(fprob) + "%" + " (" + str(fprice) +")")     
                    fibo_prob.font_size = "50%"
                    fibo_prob.font_family= "Verdana"
                    fibo_prob.stroke = fibo_line.stroke
                    fibo_prob.stroke_width = "0.5"                         
                    
                    ypos = fibo_line.y1 * 0.99
                    
                    fibo_prob.scale(1,-1)
                    plot.append( Label(fibo_prob,(xpos,ypos),0) )
                    
                    xpos += 30
        
        """
       

class FibonacciChartOld(svg.Svg):      
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
        start_date = today - datetime.timedelta( days = NUM_DAYS*resolution )
        
        values = values.samplePrices( resolution )
        prices = values.getClosePrices(start_date, today)
        
        
        min_price = min(prices)
        max_price = max(prices)
                
        price_span = max_price - min_price
        if price_span > 0:
            scaley = height / ( price_span )
        else:
            scaley = 1
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
                
              #  if l[0] > prices[-1]:
               #     continue
                    
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
                    fprice = Decimal(str(l[0])).quantize(Decimal('1.0'))
                    fibo_prob = text.Text( str(fprob) + "%" + " (" + str(fprice) +")")     
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
        month_strings = generateMonthlyStrings( start_date, today )
        
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

        p = Decimal(str(min_price))
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
    
 




