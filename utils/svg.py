
from utils import *
from core import Core
from coordinates import *
 
class AttrXmlns(object):
    def __init__ ( self ):
        self.xmlns = "http://www.w3.org/2000/svg"
    
    def __str__ ( self ):
        return str_attr ( 'xmlns', self.xmlns )

class Svg( list, 
           Core, 
           AttrXmlns, 
           AttrX, 
           AttrY,
           AttrWidth, 
           AttrHeight ):
    
    def __init__(self):
       init_bases (Svg, self)
        
    def __str__(self):
        return str_tag ( Svg, self, 'svg' )
   
def svgdoc ( svg ):
    s = '<?xml version="1.0" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        
    s += str ( svg )
    return s
    
    
    
    
    