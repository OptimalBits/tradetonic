
from attribute import *
from utils import *

class AttrFill(object):
    def __init__ ( self ):
        self.fill = None
    
    def __str__ ( self ):
        return str_attr ( 'fill', self.fill )
        
class AttrFillRule(object):
    def __init__ ( self ):
        self.fill_rule = None
    
    def __str__ ( self ):
        return str_attr ( 'fill-rule', self.fill_rule )
        
class AttrFillOpacity(object):
    def __init__ ( self ):
        self.fill_opacity = None
    
    def __str__ ( self ):
        return str_attr ( 'fill-opacity', self.fill_opacity )
        

class Fill( AttrFill, AttrFillRule, AttrFillOpacity ):
    
    def __init__ ( self ):
        init_bases (Fill, self)
    
    def __str__ ( self ):
        return str_attrs ( Fill, self )
        
   
class AttrStroke(object):
    def __init__ ( self ):
        self.stroke = None
    
    def __str__ ( self ):
        return str_attr ( 'stroke', self.stroke )
       
class AttrStrokeWidth(object):
    def __init__ ( self ):
        self.stroke_width = None
    
    def __str__ ( self ):
        return str_attr ( 'stroke-width', self.stroke_width )
        
class AttrStrokeLineCap(object):
    def __init__ ( self ):
        self.stroke_linecap = None
    
    def __str__ ( self ):
        return str_attr ( 'stroke-linecap', self.stroke_linecap )
   
class AttrStrokeLineJoin(object):
    def __init__ ( self ):
        self.stroke_linejoin = None
    
    def __str__ ( self ):
        return str_attr ( 'stroke-linejoin', self.stroke_linejoin )
        
class AttrStrokeMiterLimit(object):
    def __init__ ( self ):
        self.stroke_miterlimit = None
    
    def __str__ ( self ):
        return str_attr ( 'stroke-miterlimit', self.stroke_miterlimit )
        
class AttrStrokeDashArray(object):
    def __init__ ( self ):
        self.stroke_dasharray = None
    
    def __str__ ( self ):
        return str_attr ( 'stroke-dasharray', self.stroke_dasharray )
        
class AttrStrokeDashOffset(object):
    def __init__ ( self ):
        self.stroke_dashoffset = None
    
    def __str__ ( self ):
        return str_attr ( 'stroke', self.stroke_dashoffset )
        
class AttrStrokeOpacity(object):
    def __init__ ( self ):
        self.stroke_opacity = None
    
    def __str__ ( self ):
        return str_attr ( 'stroke-opacity', self.stroke_opacity ) 
        
class Stroke( AttrStroke,
              AttrStrokeWidth, 
              AttrStrokeLineCap, 
              AttrStrokeLineJoin, 
              AttrStrokeMiterLimit, 
              AttrStrokeDashArray, 
              AttrStrokeDashOffset,
              AttrStrokeOpacity ):
    
    def __init__ ( self ):
        init_bases (Stroke, self)
    
    def __str__ ( self ):
        return str_attrs ( Stroke, self )

class Paint ( Fill, Stroke ):
    
    def __init__(self):
        init_bases (Paint, self)

    def __str__(self):
        return str_attrs ( Paint, self )

        
           

               




