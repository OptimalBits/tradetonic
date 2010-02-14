
from utils import *
from core import Core
from coordinates import *
from paint import Paint
from transform import AttrTransform


class Rect( Core, 
            Paint,
            AttrTransform,
            AttrX, 
            AttrY, 
            AttrWidth, 
            AttrHeight, 
            AttrRx, 
            AttrRy):

    def __init__(self):
        init_bases (Rect, self)
        
    def __str__ (self):
        return str_tag ( Rect, self, 'rect' )
        
        
