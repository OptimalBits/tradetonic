
from attribute import *
from utils import *
from core import Core
from coordinates import *
from paint import Paint
from marker import AttrMarker


# note: num_coords is just used as a constraint.
def str_coords ( coords, num_coords ):
    s = ''
    for a in coords:
        if isinstance(a, tuple):
            for c in range(0,num_coords):
                s += str(a[c]) + ' '
        else:
            s += str(a) + ' '
    if len(s) > 0:
        s = s[:-1]
    return s
    
class AttrPathData(object):
    def __init__(self):
        self.d = ''
        
    def __str__ ( self ):
        return str_attr ( 'd', self.d )
        
    def moveto ( self, coords, relative = False ):
        if relative:
            self.d += 'm' 
        else:
            self.d += 'M'
          
        self.d += str_coords (coords, 2 )
            
    def close( self ):
        self.d += 'z'
        
    def lineto ( self, coords, relative = False ):
        if relative:
            self.d += 'l'
        else:
            self.d += 'L'
            
        self.d += str_coords (coords, 2 );
        
    def horizontal ( self, x, relative = False ):
        if relative:
            self.d += 'h'
        else:
            self.d += 'H'
        self.d += str (x)
        
    def vertical ( self, y, relative = False ):
        if relative:
            self.d += 'v'
        else:
            self.d += 'V'
        self.d += str (y)
        
    def curveto ( self, coords, relative = False ):
        if relative:
            self.d += 'c'
        else:
            self.d += 'C'
        
        self.d += str_coords (coords, 6 );
            
    def smooth_curveto ( self, coords, relative = False ):
        if relative:
            self.d += 's'
        else:
            self.d += 'S'
        self.d += str_coords (coords, 4 );
                      
    def quadratic_curveto ( self, coords, relative = False ):
        if relative:
            self.d += 'q'
        else:
            self.d += 'Q'
        self.d += str_coords (coords, 4 );
        
    def smooth_quadratic_curveto ( self, coords, relative = False ):
        if relative:
            self.d += 't'
        else:
            self.d += 'T'
        self.d += str_coords (coords, 2 );
        
    def arcto ( self, coords, relative = False ):
        if relative:
            self.d += 'a'
        else:
            self.d += 'A'
        self.d += str_coords (coords, 7 );
        
class Path( Core, 
            Paint,
            AttrMarker,
            AttrPathData ):

    def __init__(self):
        init_bases (Path, self)
        
    def __str__ (self):
        return str_tag ( Path, self, 'path' )
        
    
        
