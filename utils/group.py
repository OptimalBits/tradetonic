
from utils import *
from transform import AttrTransform
from core import Core
from paint import Paint


class Group( list, 
             Core,
             Paint,
             AttrTransform ):
    
    def __init__(self):
        init_bases ( Group, self )
                
    def __str__ ( self ):
        return str_tag ( Group, self, 'g' )  

        
