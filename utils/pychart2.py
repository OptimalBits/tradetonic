
import group
import path
from paint import *
from line import *
from text import *

import circle
import rect
import utils

import math
from datetime import *

SHADOW_COLOR = "#aaaaaa"
TICK_START = 1
TICK_LENGTH = -4

POINT_SIZE = 6

#
# pygraph2
#

def linearFunc( x ):
    return x

def logFunc( x ):
    return math.log( x )
    
    
# A dict of layouts
#
# 
#
class LayoutMgr:
    layout_dict = dict()
    
    def __init__( self, width, height ):
        self.width = width
        self.height = height
        
    # Use normalized coordinates [0,1]
    def addLayout( self, handle, x, y, w, h ):
        self.layout_dict[handle] = ( x, y, w, h )
    
    # return a rectangle as a tuple ( x, y, w, h, )
    def getLayout( self, handle ):
        l = self.layout_dict[handle]
        
        x = l[0] * self.width
        y = l[1] * self.height
        w = l[2] * self.width
        h = l[3] * self.height
        
        return ( x, y, w, h )
    
class Chart(object):
    rounders = [ (1,0.1),(5,0.5),(10,1),(20,2.5),(50,5),(100,10),(500,50),(1000,100),(10000,1000) ]
    
    def __init__( self, layoutMgr ):
        self.layoutMgr = layoutMgr
        self.title = None
        self.subtitle = None
    
        self.grid = None
        self.leyend = None
    
        self.xAxis = list()
        self.yAxis = list()
    
        self.plots = list()
        
    def addPlot( self ):
        pass
                
    def render( self, svg, paint ):
    
        self.render_title( svg, paint )
                
        xAxis = self.xAxis[0]
        yAxis = self.yAxis[0]
        
        plot_layout = self.layoutMgr.getLayout( 'plot' )
        
        plot_group = group.Group()
        plot_group.translate( plot_layout[0], plot_layout[1] )
        plot_group.matrix( 1, 0, 0, -1, 0, 0 )
        plot_group.translate( 0, -yAxis.length)
        
        if self.grid != None:
            self.grid.render( plot_group, paint )
                   
        for plot in self.plots:
            plot.render( plot_group )
        print plot_group
        
        xAxis.render( plot_group, paint )
        yAxis.render( plot_group, paint )
        
        svg.append( plot_group )
        
    def render_title( self, svg, paint ):
    
        if self.title != None or self.subtitle != None:
            title_layout = self.layoutMgr.getLayout( 'title' )        
            mid_point = ( title_layout[2] / 2, title_layout[3] / 3 )
            
            text_group = group.Group()
            text_group.translate( title_layout[0], title_layout[1] )
            svg.append( text_group )
    
        if self.title != None:
            
            title = Text( self.title )
            title.text_anchor = 'middle'
            title.font_family= "Arial"
            title.stroke = "black"
            title.stroke_width = "0.5"
            title.translate ( mid_point[0], mid_point[1] )
            
            text_group.append( title )
            
        if self.subtitle != None:
            subtitle = Text( self.subtitle )
            subtitle.font_size = "80%"
            subtitle.font_family= "Arial"
            subtitle.stroke = "black"
            subtitle.stroke_width = "0.5"
            subtitle.translate ( mid_point[0], mid_point[1] + 18 )
            subtitle.text_anchor = 'middle'
            
            text_group.append( subtitle )

            
    def getRounder( self, val ):
         for c in self.rounders:
            if val < c[0]:
                return c[1]
                
    def roundValueCeil( self, val, rounder ):
        return int( (val+rounder) / rounder  ) * rounder

    def roundValueFloor( self, val, rounder ):
        return int( val / rounder  ) * rounder

        
        
class TimeSeriesChart(Chart):
        
    def __init__( self, startDate, endDate, layoutMgr, useGrid = True ):
        Chart.__init__( self, layoutMgr )
        
        self.useGrid = useGrid
        self.dateLabels = self.genDateLabels( startDate, endDate )       
        print self.dateLabels

    def addPlot( self, data, paint, dates= None ):
    
        if len(self.plots) == 0:
            plotLayout = self.layoutMgr.getLayout( 'plot' )
        
            width = int( plotLayout[2] )
            height = int( plotLayout[3] )
        
            xAxis = Axis( width, 0, len(data)-1, orientation = Axis.Orientation.HORIZONTAL )
                
            xAxis.setLabels( Labels( self.dateLabels, xAxis ) )
            
            if len( self.dateLabels ) > 1:
                xAxis.setTicks( range( 0, len( self.dateLabels ) ) )
        
            self.xAxis.append( xAxis )    
            
            dataAmplitude = max(data) - min(data)
            minData = min(data) - dataAmplitude * 0.15
            if minData < 0:
                minData = 0
            
            maxData = max(data) + dataAmplitude * 0.15       

            rounder = self.getRounder( dataAmplitude )

            minData = self.roundValueFloor( minData, rounder )
            maxData = self.roundValueCeil( maxData, rounder )
        
            yAxis = Axis( height, minData, maxData, linearFunc, orientation = Axis.Orientation.VERTICAL )
        
            labels = []
            tick_value = minData
            while tick_value <= maxData:
                labels.append( '%.2f' % tick_value )
                tick_value += rounder
            
            yAxis.setTicks( range(0,len(labels) ) )            
            yAxis.setLabels( Labels( labels, yAxis ) )
        
            self.yAxis.append( yAxis )
            
            if self.useGrid: 
                self.grid = Grid( xAxis, yAxis )
                self.grid.yGrid = True

        xAxis = self.xAxis[0]
        yAxis = self.yAxis[0]
        
        len_data = float (len( data ) )
        x_coords = [ x * xAxis.length / (len_data-1) for x in range( 0, len_data ) ]

        plot = Plot( zip( x_coords, yAxis.transform( data ) ), paint )

        self.plots.append( plot )
         
    def genDateLabels( self, startDate, endDate ):
        return generateMonthlyStrings( startDate, endDate )        
        
class BarsChart(Chart):
    def __init__( self, bars, paint, layoutMgr ):
        Chart.__init__( self, layoutMgr )
       
        y, x = zip(*bars)
        
        plotLayout = self.layoutMgr.getLayout( 'plot' )
        
        width = int( plotLayout[2] )
        height = int( plotLayout[3] )
        
        xMax = max(x)
        rounder = self.getRounder( xMax )

        xMax = self.roundValueCeil( xMax, rounder )
        
        xAxis = Axis( width, 0, xMax, orientation = Axis.Orientation.HORIZONTAL )        
        
        labels = []
        tick_value = 0
        while tick_value <= xMax:
            labels.append( '%.2f' % tick_value )
            tick_value += rounder
            
        xAxis.setTicks( range(0,len(labels) ) )            
        xAxis.setLabels( Labels( labels, xAxis ) )
        
        self.xAxis.append( xAxis )
        
        yAxis = Axis( height, 0, len(y)-1, linearFunc, orientation = Axis.Orientation.VERTICAL,bias=20 )
        
        labels = []
        for bar_value in y:
            labels.append( '%.2f' % bar_value )
        
        yAxis.setLabels( Labels( labels, yAxis ) )      
        yAxis.setTicks( range(0,len(y) ) )
                
        self.yAxis.append( yAxis )
        
        self.grid = Grid( xAxis, yAxis )
        self.grid.xGrid = True
        
        x = xAxis.transform( x )
        y = yAxis.transform( range(0,len(y)) )
        
        bar_width = 10
        
        for b in zip(x,y):
            self.plots.append( Bar( 0, b[1]-bar_width/2.0, b[0], bar_width, paint ) )
                 
                 
class Bar(object):
    shadow = True

    def __init__( self, x,y, length, width, paint ):
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.paint = paint
        
    def render( self, svg ):
      
        bar_group = group.Group()
        
        if self.shadow and self.length > 0:
            shadow_paint = Paint()
            shadow_paint.fill = "#BBB"
            shadow_paint.fill_opacity = 0.6
            
            shadow = rect.Rect()    
            shadow.x = self.x
            shadow.y = self.y - 3
            shadow.width = self.length + 3
            shadow.height = self.width
            
            utils.copy_object( shadow_paint, shadow )
            
            bar_group.append( shadow )
          
        r = rect.Rect()    
        r.x = self.x
        r.y = self.y
        r.width = self.length
        r.height = self.width
        
        utils.copy_object( self.paint, r )
        bar_group.append( r )
        
        svg.append( bar_group )
          
#
# Expects layouts: title, plot, xlabels, ylabels, leyend
#
class LineChart:
    
    def __init__( self, data, layout_mgr ):
        
        self.data = data
        
        self.title = None
        self.subtitle = None
        
        self.xLabel = None
        self.yLabel = None
        
        self.layout_mgr = layout_mgr
                
        plot_layout = layout_mgr.getLayout( 'plot' )
        
        width = int( plot_layout[2] )
        height = int( plot_layout[3] )
        
        self.xAxis = Axis( width, 0, len(data)-1, orientation = Axis.Orientation.HORIZONTAL )
        self.yAxis = Axis( height, 0, 100,\
         linearFunc, orientation = Axis.Orientation.VERTICAL )
        
        self.grid = Grid( self.xAxis, self.yAxis )
        
    def setTitle( self, title, subtitle ):
        self.title = title
        self.subtitle = subtitle
        
    def setXLabel( self, label ):
        self.xLabel = label
        
    def setYLabel( self, label ):
        self.yLabel = label
        
    def render( self, svg, paint ):
    
        if self.title != None:
            title_layout = self.layout_mgr.getLayout( 'title' )
            
            mid_point = ( title_layout[2] / 2, title_layout[3] / 2 )
                          
            text_group = group.Group()
            text_group.translate( title_layout[0], title_layout[1] )
            
            title = Text( self.title )
            title.text_anchor = 'middle'
            title.font_family= "Arial"
            title.stroke = "black"
            title.stroke_width = "0.5"
            title.translate ( mid_point[0], mid_point[1] )
            
            subtitle = Text( self.subtitle )
            subtitle.font_size = "80%"
            subtitle.font_family= "Arial"
            subtitle.stroke = "black"
            subtitle.stroke_width = "0.5"
            subtitle.translate ( mid_point[0], mid_point[1] + 18 )
            subtitle.text_anchor = 'middle'
            
            text_group.extend( [title, subtitle] )

            svg.append( text_group )
            
        if self.xLabel != None:
            xlabel_layout = self.layout_mgr.getLayout( 'xlabel' )
            
            mid_point = ( xlabel_layout[2] / 2, xlabel_layout[3] / 2 )

            xlabel_group = group.Group()
            xlabel_group.translate( xlabel_layout[0], xlabel_layout[1] )
            
            label = Text( self.xLabel )
            label.text_anchor = 'middle'
            label.font_family= "Arial"
            label.stroke = "black"
            label.stroke_width = "0.5"
            label.translate ( mid_point[0], mid_point[1] )
            label.rotate( 270 )
            
            xlabel_group.append( label )
            
            svg.append( xlabel_group )
            
        if self.yLabel != None:
            ylabel_layout = self.layout_mgr.getLayout( 'ylabel' )
            
            mid_point = ( ylabel_layout[2] / 2, ylabel_layout[3] / 2 )
            
            ylabel_group = group.Group()
            ylabel_group.translate( ylabel_layout[0], ylabel_layout[1] )
            
            label = Text( self.yLabel )
            label.text_anchor = 'middle'
            label.font_family= "Arial"
            label.stroke = "black"
            label.stroke_width = "0.5"
            label.translate ( mid_point[0], mid_point[1] )
            
            ylabel_group.append( label )
            
            svg.append( ylabel_group )
        
        plot_layout = self.layout_mgr.getLayout( 'plot' )
        
        plot_group = group.Group()
        plot_group.translate( plot_layout[0], plot_layout[1] )
        svg.append( plot_group )
        
        self.render_plot( plot_group, paint )

                
    def render_plot( self, svg, paint ):
        g = group.Group()
        
        g.matrix ( 1, 0, 0, -1, 0, 0 )
        g.translate ( 0, -self.yAxis.length)
        
        plot_group = group.Group()
        
        len_data = len( self.data )-1
        x_coords = range( 0, len_data * self.xAxis.length, self.xAxis.length / len_data )
        plot = Plot( zip( x_coords, self.yAxis.transform( self.data ) ), Point.Type.CIRCLE )
    
        self.xAxis.setTicks( range(0, len( self.data )) )
        self.yAxis.setTicks( range(0, 11 ) )
    
        self.xAxis.render( plot_group, paint )
        self.yAxis.render( plot_group, paint )
        
        self.grid.render( plot_group, paint )
        
        plot.render( plot_group, paint )
        
        g.append( plot_group )
        
        svg.append( g )

        
class Axis:
    
    axe = True
    
    class Orientation:
        VERTICAL = 0
        HORIZONTAL = 1
    
    labels = None
    
    def __init__( self, length, min_val = 0, max_val = None, transformFunc = linearFunc, orientation = Orientation.HORIZONTAL, bias = 0.0 ):
        self.length = float(length)
        self.min_val = float(min_val)
        
        if max_val == None:
            max_val = length
        
        self.max_val = float(max_val)
            
        self.transformFunc = transformFunc
        self.orientation = orientation
        self.tick_positions = None
        self.bias = bias
                
    def setLabels( self, labels ):
        self.labels = labels
        
    def setTicks( self, tick_positions ):
        max_pos = max( tick_positions )
        min_pos = min( tick_positions )
        
        scale = self.length / ( float) ( max_pos - min_pos ) 
        
        self.tick_positions = []
    
        for t in tick_positions:    
            self.tick_positions.append( ( t - min_pos ) *scale + self.bias)
            
        
    def transform( self, data ):
        min_data = min(data)
        max_data = max(data)
        
        scale = self.length / ( float) ( self.max_val - self.min_val ) 
        
        bias = (min_data - self.min_val) * scale + self.bias
        
        tdata = list ()
        for x in data:
            val = ( x - min_data ) * scale + bias
            tdata.append( self.transformFunc( val ) )
            
        return tdata
        
    def render( self, svg, paint ):
        g = group.Group()
        utils.copy_object( paint, g )
        
        if self.axe:
            l = Line()
            l.x1 = 0
            l.y1 = 0
            
            if self.orientation == Axis.Orientation.HORIZONTAL:
                l.x2 = self.length + self.bias
                l.y2 = 0
            else:
                l.x2 = 0
                l.y2 = self.length + self.bias
            
            utils.copy_object( paint, l )
            
            g.append( l )
            
        if self.tick_positions != None:
            if self.orientation == Axis.Orientation.HORIZONTAL:
                for t in self.tick_positions:
                    tick = Line()
                    tick.x1 = t
                    tick.y1 = TICK_START
                    tick.x2 = t
                    tick.y2 = TICK_LENGTH
                    g.append( tick )
            
            else:
                for t in self.tick_positions:
                    tick = Line()
                    tick.x1 = TICK_START
                    tick.y1 = t
                    tick.x2 = TICK_LENGTH
                    tick.y2 = t
                    g.append( tick )
            
        if self.labels != None:
            self.labels.render( g )
            
        svg.append( g )
        
class Grid:

    xGrid = False
    yGrid = False

    def __init__( self, xAxis, yAxis ):
        self.xAxis = xAxis
        self.yAxis = yAxis
    
    def render( self, svg, paint ):
        g = group.Group()    
        utils.copy_object ( paint, g )
            
        width = self.xAxis.length + self.xAxis.bias
        height = self.yAxis.length + self.yAxis.bias
        
        if self.xGrid and self.xAxis.tick_positions != None:
            for pos in self.xAxis.tick_positions:
                h = Line ()
                h.x1 = pos
                h.y1 = 0
                h.x2 = pos
                h.y2 = height
                g.append( h )
            
        if self.yGrid and self.yAxis.tick_positions != None:
            for pos in self.yAxis.tick_positions:
                v = Line ()
                v.x1 = 0
                v.y1 = pos
                v.x2 = width
                v.y2 = pos
                g.append( v )
        
        svg.append( g )


class Labels:
    def __init__( self, labels, axis ):
        self.labels = labels
        self.axis = axis
        
    def render( self, svg ):
        g = group.Group()
        g.matrix ( 1, 0, 0, -1, 0, 0 )
        
        g.fill = g.stroke
        
        i = 0
        
        if self.axis.tick_positions != None:
            positions = self.axis.tick_positions
        else:
            positions = [0]
        
        for p in positions:
            label = Text( str(self.labels[i]) )
            label.text_anchor = 'middle'
            label.font_family= "Arial"
            label.stroke = "gray"
            label.fill = "gray"
            label.stroke_width = "0.1"
            label.font_size = "70%"
                
            if self.axis.orientation == Axis.Orientation.HORIZONTAL:
                label.translate ( p, 20 )
                label.rotate ( 330 )
                
            elif self.axis.orientation == Axis.Orientation.VERTICAL:
                label.translate ( -25, -p )
                    
            
            g.append( label )
                
            i = i + 1
                
        svg.append( g )
        
        
class Ticks:
    def __init__( self, tick_generator, orientation = Axis.Orientation.HORIZONTAL ):
        self.generator = tick_generator
        self.orientation = orientation
        
    def render( self, svg ):
        pass
                
            
class Plot:
    shadow = True
    point_type = None

    def __init__( self, coords, paint ):
        self.coords = coords
        self.paint = paint
        
    def render( self, svg ):
      
        plot_line = group.Group()
    
        if self.shadow and self.paint.stroke_width != None:
            shadow_paint = Paint()
            shadow_paint.stroke_width = self.paint.stroke_width * 2
            shadow_paint.stroke = SHADOW_COLOR
            p = path.Path ()

            utils.copy_object ( shadow_paint, p )
            p.moveto ( [ (c[0],c[1]-(shadow_paint.stroke_width-1)) for c in self.coords ] )
            plot_line.append( p )
        
        if self.paint.fill != None:
            paint = Paint( fill = self.paint.fill )
            p = path.Path ()    
            p.moveto ( self.coords )
            p.vertical( 0 )
            p.horizontal( 0 )
            p.close()
            utils.copy_object( paint, p )
            plot_line.append( p )
            
        paint = Paint()
        utils.copy_object( self.paint, paint )
        
        paint.fill = "None"
        
        p = path.Path()    
        p.moveto( self.coords )
    
        utils.copy_object( paint, p )
        plot_line.append( p )
        
        svg.append( plot_line )
        
        plot_points = group.Group()
        utils.copy_object ( paint, plot_points )
        plot_points.fill = plot_points.stroke
        
        if self.point_type != None:
            for coord in self.coords:
                point = Point( coord, POINT_SIZE, self.point_type )
            
                point.render( plot_points )
            svg.append( plot_points )
                
class Point:
    class Type:
        NONE = 0
        CIRCLE = 1
        TRIANGLE = 2
        SQUARE = 3
        DIAMANT = 4
        
    def __init__( self, coord, size, point_type = Type.CIRCLE ):
        self.coord = coord
        self.size = size
        self.point_type = point_type
        
    def render( self, svg ):
        if self.point_type == Point.Type.CIRCLE:
            c = circle.Circle()
            c.cx = self.coord[0]
            c.cy = self.coord[1]
            c.r = self.size / 2
            svg.append( c )

        elif self.point_type == Type.TRIANGLE:
            pass
        elif self.point_type == Type.SQUARE:
            pass
        elif self.point_type == Type.DIAMANT:
            pass


# --------- Utils ---------
def generateMonthlyStrings( startDate, endDate ):
    year = startDate.year
    endYear = endDate.year
        
    month = startDate.month
    endMonth = endDate.month

    labels = list()
    while year < endYear or month <= endMonth:
        d = date(year, month, 1)
        
        if month == 1:
            format = "%b %y"
        else:
            format = "%b"            
              
        dateString = d.strftime (format)
            
        labels.append(dateString)
        
        month += 1
        if month > 12:
            month = 1
            year += 1
                            
    return labels

def datetimeIterator(from_date=datetime.now(), to_date=None, delta=timedelta(minutes=1) ):
    while to_date is None or from_date <= to_date:
        yield from_date
        from_date = from_date + delta
    return
    
    

