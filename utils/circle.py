
from attribute import *
from utils import *
from core import Core
from coordinates import *
from paint import Paint
        
class Circle( Core, 
              Paint,
              AttrCx,
              AttrCy,
              AttrR ):

    def __init__(self):
        init_bases (Circle, self)
        
    def __str__ (self):
        return str_tag ( Circle, self, 'circle' )
        
    
        
