
from core import Core
from utils import init_bases, str_attrs, str_tag
from attribute import *
from coordinates import AttrViewbox

class AttrMarkerStart(object):
    def __init__ ( self, marker_start = None ):
        self.marker_start = marker_start
    
    def __str__ ( self ):
        return str_attr ( 'marker-start', self.marker_start ) 

class AttrMarkerEnd(object):
    def __init__ ( self, marker_end = None ):
        self.marker_end = marker_end
    
    def __str__ ( self ):
        return str_attr ( 'marker-end', self.marker_end )

class AttrMarkerMid(object):
    def __init__ ( self, marker_mid = None ):
        self.marker_mid = marker_mid
    
    def __str__ ( self ):
        return str_attr ( 'marker-mid', self.marker_mid ) 

class AttrMarker( AttrMarkerStart, 
                  AttrMarkerEnd, 
                  AttrMarkerMid ):
    def __init__(self, **kwargs):
        init_bases ( AttrMarker, self, **kwargs )
        
    def __str__ (self):
        return str_attrs ( AttrMarker, self )

class AttrMarkerUnits(object):
    def __init__ ( self, markerUnits = None ):
        self.markerUnits = markerUnits
    
    def __str__ ( self ):
        return str_attr ( 'markerUnits', self.markerUnits ) 

class AttrRefX(object):
    def __init__ ( self, refX = None ):
        self.refX = refX
    
    def __str__ ( self ):
        return str_attr ( 'refX', self.refX ) 

class AttrRefY(object):
    def __init__ ( self, refY = None ):
        self.refY = refY
    
    def __str__ ( self ):
        return str_attr ( 'refY', self.refY ) 


class AttrMarkerWidth(object):
    def __init__ ( self, markerWidth = None ):
        self.markerWidth = markerWidth
    
    def __str__ ( self ):
        return str_attr ( 'markerWidth', self.markerWidth ) 

class AttrMarkerHeight(object):
    def __init__ ( self, markerHeight = None ):
        self.markerHeight = markerHeight
    
    def __str__ ( self ):
        return str_attr ( 'markerHeight', self.markerHeight ) 

class AttrOrient(object):
    def __init__ ( self, orient = "auto" ):
        self.orient = orient
    
    def __str__ ( self ):
        return str_attr ( 'orient', self.orient ) 
     
class Marker(list,
             Core,
             AttrMarkerUnits,
             AttrRefX,
             AttrRefY,
             AttrMarkerWidth,
             AttrMarkerHeight,
             AttrOrient,
             AttrViewbox):
    def __init__(self, **kwargs):
        init_bases (Marker, self, **kwargs)
    
    def __str__ (self):
        return str_tag ( Marker, self, 'marker' )
        
        
        
   