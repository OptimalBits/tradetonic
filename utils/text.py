
from utils import *
from core import Core
from coordinates import *
from paint import Paint
from transform import AttrTransform


class AttrFontFamily(object):
    def __init__ ( self ):
        self.font_family = None
        
    def __str__ ( self ):
        return str_attr ( 'font-family', self.font_family )

class AttrFontSize(object):
    def __init__ ( self ):
        self.font_size = None
        
    def __str__ ( self ):
        return str_attr ( 'font-size', self.font_size )
    
class AttrFontWeight(object):
    def __init__ ( self ):
        self.font_weight = None
        
    def __str__ ( self ):
        return str_attr ( 'font-weight', self.font_weight )
        
class AttrFontStyle(object):
    def __init__ ( self ):
        self.font_style = None
        
    def __str__ ( self ):
        return str_attr ( 'font-style', self.font_style )


class Text( Core, 
            Paint,
            AttrTransform,
            AttrFontFamily,
            AttrFontSize,
            AttrFontWeight,
            AttrFontStyle ):

    def __init__(self, text_string ):
        init_bases (Text, self)
        self.text_string = text_string
        
    def __str__ (self):
        s = '<text '
        s += str_attrs ( Text, self )
        s += '>'
        
        s += self.text_string
        s += '</text>'
        return s
        
        
        
        
        
