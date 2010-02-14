#from django.db import models

def find_tab( tabs, name ):
    for t in tabs:
        if t.name == name:
            return t
            
def select_tab( tabs, name ):
    for t in tabs:
        if t.name == name:
            t.select()
            r = t
        else:
            t.deselect()
    return r

class Tab(object):
    def __init__( self, name, relativeUrl, view, subtabs = ()):
        self.name = name
        self.relativeUrl = relativeUrl
        self.subtabs = subtabs
        self.view = view
        
        self.parent = None
        for t in subtabs:
            t.parent = self
        
        self.selected = False
        self.enabled = True
        
    def url( self ):
        if self.parent != None:
            return self.parent.url() + "/" + self.relativeUrl
        else:
            return self.relativeUrl
            
    def url_pattern( self, tabs ):
        #if isinstance(self.view, list):
        if len(self.subtabs) > 0:
            p = ( r'^' + self.url() + "/", self.view, {'tabs':tabs} )
        else:
            p = ( r'^' + self.url() + r'$', self.view, {'tabs':tabs} )
        return p

    def has_subtabs( self ):
        return len(self.subtabs) > 0

    def deselect( self ):
        self.selected = False
        
    def select( self ):
        self.selected = True
        
    def enable( self ):
        self.enabled = True
    
    def disable( self ):
        self.enabled = False
        
