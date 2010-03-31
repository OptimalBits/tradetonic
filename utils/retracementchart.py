
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

NUM_DAYS = 20

class RetracementLevelsChart(svg.Svg):      
       def __init__ ( self, id, title, desc, values ):
        svg.Svg.__init__(self)
        
        self.id = id
        self.setXmlSpace (True)
        self.setXmlLang ("english")
        
        width = 430
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

class retracementPatternChart(svg.Svg):
    def __init__ ( self, title, desc, pattern ):
        svg.Svg.__init__(self)
        
        self.setXmlSpace(True)
        self.setXmlLang("english")
        
        width = 420
        height = 300
        
        layoutMgr = LayoutMgr( width, height )

        layoutMgr.addLayout('plot', 0.1, 0.2, 0.8, 0.6 )
        layoutMgr.addLayout('title', 0.0, 0.0, 1.0, 0.2 )
        layoutMgr.addLayout('xlabel', 0.0, 0.1, 0.1, 0.8)

        layoutMgr.addLayout('ylabel', 0.1, 0.8, 0.8, 0.2)
        
        import datetime
        today = datetime.date.today()
        start_date = today - datetime.timedelta( days = NUM_DAYS )
        
        tsc = TimeSeriesChart( start_date, today, layoutMgr, True )
        tsc.title = title
        tsc.subtitle = desc
        
        p = Paint ()
        p.stroke = "blue"
        p.fill = "gray" #plotGradient.getURI()

        tsc.addPlot( pattern, p )
        
        p = Paint ()
        p.stroke = "gray"
       
        tsc.render( self, p )

         
class FibonacciChart(svg.Svg):      
       def __init__ ( self, title, desc, values, levels, resolution = 1 ):
        svg.Svg.__init__(self)
        
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
        plotGradient.append( GradientStop( offset=0.5, stop_color="#CCE", stop_opacity=0.5) )
        self.append( plotGradient )

        # Chart
        import datetime
        today = datetime.date.today()
        start_date = today - datetime.timedelta( days = NUM_DAYS*resolution )
        
        tsc = TimeSeriesChart( start_date, today, layoutMgr )
        tsc.title = title
        tsc.subtitle = desc
       
        # Plot
        p = Paint ()
        p.stroke = "blue"
        p.fill = plotGradient.getURI()
        
        values = values.samplePrices( resolution )
        prices = values.getClosePrices(start_date, today)
        
        tsc.addPlot( prices, p )
        min_price = min(prices)
        max_price = max(prices)
        last_price = prices[-1]
        going_short = levels[0][0] > levels[1][0]

        p2 = Paint ()
       # p2.stroke_dasharray = "2"
        
        prob = 0
        xpos = 10
        startColor = (0,255,0)
        endColor = (255, 0, 0)
        for l in levels:
            if l[0] > 0:
                prob += l[1]
                             
                if (going_short and last_price >= l[0]) or ( not going_short and last_price <= l[0]):
                    p2.stroke = interpColor( startColor, endColor, prob )
                    tsc.addPlot( [l[0],l[0]], p2 )
                
   
        p = Paint ()
        p.stroke = "gray"
        p.fill = "none"
        p.stroke_width = 0.5

        tsc.render( self, p )

def interpColor( startColor, endColor, prob ):
    t = prob / 100.0
    a = startColor[0] * ( 1 - t ) + endColor[0] * t
    b = startColor[1] * ( 1 - t ) + endColor[1] * t
    c = startColor[2] * ( 1 - t ) + endColor[2] * t
    
    return "#%02x%02x%02x" % (a,b,c)
    
 




