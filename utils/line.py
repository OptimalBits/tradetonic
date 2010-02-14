
from attribute import *
from utils import *
from core import Core
from coordinates import *
from paint import Paint
        
class Line( Core, 
            Paint,
            AttrX1,
            AttrY1,
            AttrX2,
            AttrY2 ):

    def __init__(self):
        init_bases (Line, self)
        
    def __str__ (self):
        return str_tag ( Line, self, 'line' )
        
    
        
