
from attribute import *


class AttrViewbox( object ):
    def __init__( self, viewBox = None ):
        self.viewBox = viewBox
    def __str__ ( self ):
        return str_attr ( 'viewBox', self.viewBox )


class AttrX(object):
    def __init__ ( self ):
        self.x = None
        
    def __str__ ( self ):
        return str_attr ( 'x', self.x )

        
class AttrY(object):
    def __init__ ( self ):
        self.y = None
    
    def __str__ ( self ):
        return str_attr ( 'y', self.y )
        
class AttrX1(object):
    def __init__ ( self ):
        self.x1 = None
        
    def __str__ ( self ):
        return str_attr ( 'x1', self.x1 )

        
class AttrY1(object):
    def __init__ ( self ):
        self.y1 = None
    
    def __str__ ( self ):
        return str_attr ( 'y1', self.y1 )
        
        
class AttrX2(object):
    def __init__ ( self ):
        self.x2 = None
        
    def __str__ ( self ):
        return str_attr ( 'x2', self.x2 )

        
class AttrY2(object):
    def __init__ ( self ):
        self.y2 = None
    
    def __str__ ( self ):
        return str_attr ( 'y2', self.y2 )
        
        
class AttrWidth(object):
    def __init__ ( self ):
        self.width = None
    
    def __str__ ( self ):
        return str_attr ( 'width', self.width )
             
class AttrHeight(object):
    def __init__ ( self ):
        self.height = None
    
    def __str__ ( self ):
        return str_attr ( 'height', self.height )
        
        
class AttrRx(object):
    def __init__ ( self ):
        self.rx = None
    
    def __str__ ( self ):
        return str_attr ( 'rx', self.rx )
        
        
class AttrRy(object):
    def __init__ ( self ):
        self.ry = None
    
    def __str__ ( self ):
        return str_attr ( 'ry', self.ry )
        
class AttrCx(object):
    def __init__ ( self ):
        self.cx = None
        
    def __str__ ( self ):
        return str_attr ( 'cx', self.cx )

        
class AttrCy(object):
    def __init__ ( self ):
        self.cy = None
    
    def __str__ ( self ):
        return str_attr ( 'cy', self.cy )
        
class AttrR(object):
    def __init__ ( self ):
        self.r = None
    
    def __str__ ( self ):
        return str_attr ( 'r', self.r )

