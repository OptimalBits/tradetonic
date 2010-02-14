
from utils import *

class AttrId(object):
    def __init__ ( self ):
        self.name = None

    def setId ( self, name ):
        self.name = name
        
    def __str__ ( self ):
        if self.name != None:
            return ' id="' + self.name + '"'
        else:
            return ''
        
class AttrXmlBase(object):
    def __init__ ( self ):
        self.uri = None
    
    def setXmlBase ( self, uri ):
        self.uri = None
        
    def __str__ ( self ):
        if self.uri != None:
            return ' xml:base="' + self.uri +  '"'
        else:
            return ''
        
class AttrXmlLang(object):
    def __init__ ( self ):
        self.languageId = None
    
    def setXmlLang ( self, languageId ):
        self.languageId = languageId
    
    def __str__ ( self ):
        if self.languageId != None:
            return ' xml:lang="' + self.languageId +  '"'
        else:
            return ''

class AttrXmlSpace(object):
    def __init__ ( self, default = True ):
        self.default = None
    
    def setXmlSpace ( self, default = True ):
        self.default = default
    
    def __str__ ( self ):
        if self.default != None:
            if self.default == True:
                return ' xml:space="default"'
            else:
                return ' xml:space="preserve"'
        return ''

class Core (AttrId, AttrXmlBase, AttrXmlLang, AttrXmlSpace):
    def __init__(self):
        init_bases ( Core, self)
        
    def __str__ (self):
        return str_attrs ( Core, self )

