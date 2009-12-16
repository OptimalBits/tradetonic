
import svg
import path
import line
import group
import text
import paint
import utils
import rect
from datetime import *

from paint import *

class Viewport(object):
    def __init__( self, x, y, w, h ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
class Object(group.Group):
    def __init__(self, viewport = None ):
        group.Group.__init__(self)
        
        if viewport == None:
            self.viewport = Viewport( 0.0, 0.0, 1.0, 1.0 )
        else:
            self.viewport = viewport
        
    """    
    def scaleToViewport(self, viewport):
        scalex = float(viewport.w) / self.viewport.w; 
        scaley = float(viewport.h) / self.viewport.h;
        
        self.translate( viewport.x, viewport.y )
        self.scale( scalex, scaley )
    """
    
class Container(group.Group):
    def __init__( self, viewport ):
        group.Group.__init__(self)
        self.viewport = viewport
        
    def append( self, obj ):
        
        self.viewport.x = min(self.viewport.x, obj.viewport.x)
        self.viewport.y = min(self.viewport.y, obj.viewport.y)
        self.viewport.w = max(self.viewport.w, obj.viewport.w)
        self.viewport.h = max(self.viewport.h, obj.viewport.h)
    
        group.Group.append( self, obj )


class Chart(Container):
    def __init__ ( self, viewport, axis ):
        Container.__init__(self, viewport)
        
        self.matrix ( 1, 0, 0, -1, 0, 0 )
        self.translate ( 0, -viewport.h * 2)
         
        self.extend ([ axis[0], axis[1] ])
     
    #    if grid:
    #        p = paint.Paint ()
    #        p.stroke_width = "0.2"
    #        p.stroke = "#808080"
        
    #        self.append( Grid( viewport, axis[0].tickInterval, axis[1].tickInterval, p ) )


class BarsChart(Chart):
    def __init__ ( self, values, vertical = False, grid = False ):
            
        r = rect.Rect()
        r.x = 0
        r.y = 0
        r.width = 10
        r.height = 10
        r.rx = 0
        
        b = Bars( r, values, vertical )
           
        p = Paint ()
        p.fill ="red"
        p.stroke = "black"
        p.stroke_width = 2
       
        if vertical:
            axisx_length = b.viewport.h
            axisy_length = b.viewport.w
        else:
            axisx_length = b.viewport.w
            axisy_length = b.viewport.h
        
        axis = ( AxisX ( axisx_length, 25, None, p ), 
                 AxisY ( axisy_length, 25, None, p ) )
 
        Chart.__init__( self, b.viewport, axis, grid )
        
        self.append( b )


class RetracementLevelsChart(Chart):
       def __init__ ( self, values ):
            
        r = rect.Rect()
        r.x = 0
        r.y = 0
        r.width = 10
        r.height = 10
        r.rx = 0
        
        b = Bars( r, values, True )
           
        p = Paint ()
        p.fill ="red"
        p.stroke = "grey"
        p.stroke_width = 2
        
        axisx_length = 100
        axisy_length = len(values)
        
        axis = ( AxisX ( axisx_length, 25, None, p ), 
                 AxisY ( axisy_length, 1, None, p ) )
 
        Chart.__init__( self, b.viewport, axis )
        
        #grid = Grid( b.viewport, 25, 1, p )
        #self.append(grid)
        
        self.append( b )


#
# Plots a graph
#
class Plot (group.Group):
    def __init__(self, data, paint ):
        group.Group.__init__(self)
        p = path.Path ()
        utils.copy_object ( paint, self )
        
        p.fill ="none"
        p.moveto ( data )
        
        self.append ( p )
        
#
# Draws a grid
# area ( x0,y0, w, h )
#
class Grid(Object):
    def __init__ (self, viewport, gw, gh, paint ):
        Object.__init__(self, viewport)        
        utils.copy_object ( paint, self )
            
        # draw
        num_lines = int (viewport.w / gw) - 1
        x = viewport.x + gw
        for l in range ( 0, num_lines ):
            v = line.Line ()
            v.x1 = x
            v.y1 = viewport.y
            v.x2 = x
            v.y2 = v.y1 + viewport.h    
                
            x += gw
            self.append (v)          
            
        num_lines = int ( viewport.h / gh) - 1
        y = viewport.y + gh
        for l in range (0, num_lines ):
            h = line.Line ()
            h.x1 = viewport.x
            h.y1 = y
            h.x2 = h.x1 + viewport.w
            h.y2 = y    
                
            y += gh
            self.append (h)
            
class Tick(group.Group):
    def __init__ (self):
        group.Group.__init__ (self)
        l = line.Line ()
        l.x1 = 0
        l.y1 = -3
        l.x2 = 0
        l.y2 = 3
        
        self.append ( l )
            
class Ticks(group.Group):
    def __init__ (self, length, interval, tick = None):
        group.Group.__init__( self )
        if tick == None:
            tick = Tick
        
        for t in self.ticks( length, interval, tick ):
            self.append( t )
            
    def ticks( self, length, interval, tick ):
        numTicks = int( length / interval ) + 1
        x = 0
        for t in range (0,numTicks):
            new_tick = tick()
            new_tick.translate ( x, 0 )
            x += interval
            yield new_tick
            

class Leyend(object):
    pass
      
class Label(group.Group):
    def __init__ ( self, text, coord, angle = 0 ):
        group.Group.__init__(self)
        self.append ( text )
        self.translate ( coord[0], coord[1] )
        if angle != 0:
            self.rotate ( angle )
            
#
# Generate a list of labels for some date interval.
#
class DateLabels(group.Group):
    def __init__ ( self, startDate, endDate, delta, format ):
        group.Group.__init__(self)
        coord = ( 0, 0 ) 
        for date in datetimeIterator ( startDate, endDate, delta[0] ):
            dateString = text.Text (date.strftime (format))
            coord = ( coord[0] + delta[1], coord[1] + delta[2] )
            self.append ( Label ( dateString, coord, 0 ) )
            
            
def generateMonthlyStrings( startDate, endDate ):
    year = startDate.year
    endYear = endDate.year
        
    month = startDate.month
    endMonth = endDate.month

    labels = list()
    while year < endYear or month < endMonth:
        d = date(year, month, 1)
        
        if month == 1:
            format = "%b %y"
        else:
            format = "%b"            
              
        dateString = text.Text (d.strftime (format))
            
        labels.append(dateString)
        
        month += 1
        if month > 12:
            month = 1
            year += 1
                            
    return labels
                     
#
# Class Bars 
#
# bars - List of bar objects to be used as templates.
# This objects should have normalized coordinates ( range 0.0-1.0 )
#
# Values - A list of tupples, where every element has the value for
# one of the bars. Every tupple should have same number of elements 
# as the bars list.
#

class Bars( Object ):
    def __init__( self, bar, values, vertical = False ):
        from copy import copy
        
        x, y = zip(*values)
        
        maxx, minx = ( max(x), min(x) )
        maxy, miny = ( max(y), min(y) )
        
        width = maxx - minx
        height = ( maxy - miny ) * bar.height
        
        Object.__init__( self, Viewport( 0, 0, width, height ) )
        
        self.matrix ( 1, 0, 0, -1, 0, 0 )
        
        if vertical:
            self.rotate( -90 )
        else:
            self.translate( 0, -height )
        
        T = 0
        for t in values:
            b = copy(bar)
            b.translate( T, 0 )
            b.scale( 1, t[1] )
            self.append( b )
            T = T + 20
        
#
# Represents and draws an axis.
#
class Axis(group.Group):
    def __init__ ( self, origin, length, tickInterval, paint ):
        group.Group.__init__(self)
        utils.copy_object ( paint, self )
        
        self.tickInterval = tickInterval
        
        self.line = line.Line()
                
        self.line.x1 = 0
        self.line.y1 = 0
        self.line.x2 = length
        self.line.y2 = 0
        self.length = length
        
        self.translate( origin[0], origin[1] )
        
        self.line.fill ="none"
        self.append ( self.line )
        ticks = Ticks ( length, tickInterval )

        self.append ( ticks )
        
#
# x_range ( star_x, end_x )
# labels ( x, label )
#
class AxisX( Axis ):
    def __init__ ( self, origin, length, tickInterval, paint ):
        Axis.__init__ ( self, origin, length, tickInterval, paint ) 
        
class AxisY( Axis ):
    def __init__ ( self, origin, length, tickInterval, paint ):
        Axis.__init__ ( self, origin, length, tickInterval, paint )
        self.rotate ( -90 )  
       
#
# A simple Bar object.
#
class Bar(group.Group):
    def __init__( self ):
        r = rect.Rect()
        r.x = 1.0
        r.y = 1.0
        r.width = 1.0
        r.height = 1.0
        r.rx = 20
        
        self.append( r )
         
class Histogram(object):
    def __init__( self, values, numBins ):
        self.hist = [ 0 for x in range(length(values)) ]
        
        min_val = min( values )
        max_val = max( values )
        
        for x in values:
            bin = round ( ( (float) (x - min_val) / max_val ) / numBins )
        

def datetimeIterator(from_date=datetime.now(), to_date=None, delta=timedelta(minutes=1) ):
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + delta
    return

            

