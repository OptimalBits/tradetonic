
import group
import line

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
            
    def logTicks( self, length, interval, tick, scaleFunc ):
    	pass
	
