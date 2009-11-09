
from attribute import *
        
class AttrTransform(object):
    def __init__ ( self ):
        self.s = ''
        
    def __str__ (self):
        if len(self.s) > 0:
            return str_attr( 'transform', self.s[:-1] )
        else:
            return ''
        
    def matrix ( self, a, b, c, d, e, f ):
        self.s += 'matrix(' + \
                  str(a) + ',' + \
                  str(b) + ',' + \
                  str(c) + ',' + \
                  str(d) + ',' + \
                  str(e) + ',' + \
                  str(f) + \
                  ')  '

    def translate ( self, tx, ty = None ):
        self.s += 'translate(' + str(tx)
        if ty != None:
            self.s += ',' + str(ty)
        self.s += ') '
    
    def scale ( self, sx, sy = None ):
        self.s += 'scale(' + str(sx)
        if sy != None:
            self.s += ',' + str(sy)
        self.s += ') '
        
    def rotate (self,  angle, cx = None, cy = None ):
        self.s += 'rotate(' + str(angle)
        if cx != None and cy != None:
            self.s += "," + str(cx) + ',' + str(cy)
        self.s += ') '
            
    def skewX ( self, angle ):
        self.s += 'skewX(' + str (angle) + ') '
        
    def skewY ( self, angle ):
        self.s += 'skewY(' + str (angle) + ') '
        
