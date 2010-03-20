
from utils import *

class AttrId(object):
    def __init__ ( self, id = None ):
        self.id = id
        
    def __str__ ( self ):
        if self.id != None:
            return ' id="' + self.id + '"'
        else:
            return ''
            
    def getURI( self ):
    	return "url(#" + str(self.id) + ")"
        
class AttrXmlBase(object):
    def __init__ ( self, uri = None ):
        self.uri = uri
    
    def setXmlBase ( self, uri ):
        self.uri = None
        
    def __str__ ( self ):
        if self.uri != None:
            return ' xml:base="' + self.uri +  '"'
        else:
            return ''
        
class AttrXmlLang(object):
    def __init__ ( self, languageId = None ):
        self.languageId = languageId
    
    def setXmlLang ( self, languageId ):
        self.languageId = languageId
    
    def __str__ ( self ):
        if self.languageId != None:
            return ' xml:lang="' + self.languageId +  '"'
        else:
            return ''

class AttrXmlSpace(object):
    def __init__ ( self, default = None ):
        self.default = default
    
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
    def __init__(self, **kwargs):
        init_bases ( Core, self, **kwargs )
        
    def __str__ (self):
        return str_attrs ( Core, self )

