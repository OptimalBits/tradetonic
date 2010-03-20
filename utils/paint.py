
from attribute import *
from utils import *

class AttrFill(object):
    def __init__ ( self, fill = None ):
        self.fill = fill
    
    def __str__ ( self ):
        return str_attr ( 'fill', self.fill )
        
class AttrFillRule(object):
    def __init__ ( self, fill_rule = None ):
        self.fill_rule = fill_rule
    
    def __str__ ( self ):
        return str_attr ( 'fill-rule', self.fill_rule )
        
class AttrFillOpacity(object):
    def __init__ ( self, fill_opacity=None ):
        self.fill_opacity = fill_opacity
    
    def __str__ ( self ):
        return str_attr ( 'fill-opacity', self.fill_opacity )
        

class Fill( AttrFill, AttrFillRule, AttrFillOpacity ):
    
    def __init__ ( self, **kwargs ):
        init_bases (Fill, self, **kwargs)
    
    def __str__ ( self ):
        return str_attrs ( Fill, self )
        
   
class AttrStroke(object):
    def __init__ ( self, stroke = None ):
        self.stroke = stroke
    
    def __str__ ( self ):
        return str_attr ( 'stroke', self.stroke )
       
class AttrStrokeWidth(object):
    def __init__ ( self, stroke_width = None ):
        self.stroke_width = stroke_width
    
    def __str__ ( self ):
        return str_attr ( 'stroke-width', self.stroke_width )
        
class AttrStrokeLineCap(object):
    def __init__ ( self, stroke_linecap = None ):
        self.stroke_linecap = stroke_linecap
    
    def __str__ ( self ):
        return str_attr ( 'stroke-linecap', self.stroke_linecap )
   
class AttrStrokeLineJoin(object):
    def __init__ ( self, stroke_linejoin = None ):
        self.stroke_linejoin = stroke_linejoin
    
    def __str__ ( self ):
        return str_attr ( 'stroke-linejoin', self.stroke_linejoin )
        
class AttrStrokeMiterLimit(object):
    def __init__ ( self, stroke_miterlimit = None ):
        self.stroke_miterlimit = stroke_miterlimit
    
    def __str__ ( self ):
        return str_attr ( 'stroke-miterlimit', self.stroke_miterlimit )
        
class AttrStrokeDashArray(object):
    def __init__ ( self, stroke_dasharray = None ):
        self.stroke_dasharray = stroke_dasharray
    
    def __str__ ( self ):
        return str_attr ( 'stroke-dasharray', self.stroke_dasharray )
        
class AttrStrokeDashOffset(object):
    def __init__ ( self, stroke_dashoffset = None ):
        self.stroke_dashoffset = None
    
    def __str__ ( self ):
        return str_attr ( 'stroke', self.stroke_dashoffset )
        
class AttrStrokeOpacity(object):
    def __init__ ( self, stroke_opacity = None ):
        self.stroke_opacity = stroke_opacity
    
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
    
    def __init__ ( self, **kwargs ):
        init_bases (Stroke, self, **kwargs)
    
    def __str__ ( self ):
        return str_attrs ( Stroke, self )

class Paint ( Fill, Stroke ):
    
    def __init__(self, **kwargs):
        init_bases (Paint, self, **kwargs)

    def __str__(self):
        return str_attrs ( Paint, self )

        
           

               




