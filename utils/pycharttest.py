
from paint import *
from pychart2 import *
from gradient import *
from svg import *

layoutMgr = LayoutMgr( 640, 480 )

layoutMgr.addLayout('plot', 0.1, 0.2, 0.8, 0.6 )
layoutMgr.addLayout('title', 0.0, 0.0, 1.0, 0.2 )
layoutMgr.addLayout('xlabel', 0.0, 0.1, 0.1, 0.8)

layoutMgr.addLayout('ylabel', 0.1, 0.8, 0.8, 0.2)

a = LineChart( [ 10, 34, 12, 15, 67, 49, 56, 23, 15, 28, 6 ], layoutMgr )

a.setTitle( "Monthly Average Temperature", "Source: World Climate" )
a.setXLabel( "Temperature" )
a.setYLabel( "Last year..." )

labels = Labels( ["Jan","Feb","Mars", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
				 a.xAxis )

a.xAxis.setLabels( labels )

labels = Labels( [ 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110 ], a.yAxis )
a.yAxis.setLabels( labels )

svg = Svg()

#data = [ 27, 34, 12, 45, 87, 49, 56, 23, 15, 28, 60 ]
#data = [ 27.3, 24.6, 22.2, 25.6, 22.4, 23.1, 25.4, 23, 22.4, 28, 20 ]
data = [ 3.3, 3.6, 3.2, 3.6, 3.4, 3.1, 3.4, 3, 3.4, 3, 3.1 ]



#b = TimeSeriesChart( datetime(2009,4,3, 9), datetime(2010,4,3, 9), layoutMgr )

# Add a plot
plotGradient = LinearGradient()
plotGradient.id = "plotGradient"
plotGradient.x2 = 0
plotGradient.y2 = 1

plotGradient.append( GradientStop( offset=0.0, stop_color="#889") ) 
plotGradient.append( GradientStop( offset=0.5, stop_color="#CCE") )
plotGradient.append( GradientStop( offset=1.0, stop_color="#889") )
svg.append( plotGradient )

plotPaint = Paint()
plotPaint.fill = plotGradient.getURI()
plotPaint.stroke = "gray"

#b.addPlot( data, plotPaint )
#b.addPlot( [4,3,1,2,3,4,3,2,3,4,3,2,3,2,1,2,3,4,2,2,3,4,3,2,3,2,3,1,2,3], plotPaint )

c = BarsChart( [(0,4),(1,8),(2,2),(3,10),(4,15),(5,4),(2,3),(7,24),(4,10)],plotPaint, layoutMgr )
c.title = "These are the nice odds"
c.subtitle = "Or at least I think so"

#


svg.id = "My Chart Test"
svg.setXmlSpace (True)
svg.setXmlLang ("english")

svg.width = 640
svg.height = 480

p = Paint ()
p.fill = "none"
p.stroke = "red"
p.stroke_width = 0.2

c.render( svg, p )

f = open ( 'test.svg', 'wb' )
f.write ( svgdoc(svg) )
f.close()

