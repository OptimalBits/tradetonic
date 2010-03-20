
from core import Core
from coordinates import *
from utils import *

class LinearGradient( list,
                      Core,
                      AttrX1,
                      AttrY1,
                      AttrX2,
                      AttrY2 ):
    def __init__(self, **kwargs ):
        init_bases (LinearGradient, self, **kwargs)
        
    def __str__ (self):
        return str_tag ( LinearGradient, self, 'linearGradient' )

class AttrOffset(object):
    def __init__ ( self, offset = None ):
        self.offset = offset
    
    def __str__ ( self ):
        return str_attr ( 'offset', self.offset )
        
class AttrStopColor(object):
    def __init__ ( self, stop_color = None ):
        self.stop_color = stop_color
    
    def __str__ ( self ):
        return str_attr ( 'stop-color', self.stop_color )
        
class AttrStopOpacity(object):
    def __init__ ( self, stop_opacity = None ):
        self.stop_opacity = stop_opacity
    
    def __str__ ( self ):
        return str_attr ( 'stop-opacity', self.stop_opacity ) 
    
class GradientStop( Core,
                    AttrOffset,
                    AttrStopColor,
                    AttrStopOpacity ):
    def __init__( self, **kwargs ):
        init_bases ( GradientStop, self, **kwargs )
        
    def __str__(self):
        return str_tag ( GradientStop, self, 'stop' )
        
        
        
        