

def str_tag ( cls, obj, tagname ):
    s = '<' + tagname
    for attr in cls.__bases__:
        if attr != list:
            s += attr.__str__(obj)
    
    if isinstance (obj,list):
        s += '>\n'
        for e in obj:
            s += str ( e )
        s += '</' + tagname + '>\n'
    else:
        s += '/>\n'
    
    return s
        
def str_attrs ( cls, obj ):
    s = ''
    for attr in cls.__bases__:
        s += attr.__str__(obj)
    return s
    
def init_bases ( cls, obj ):
    for attr in cls.__bases__:
        attr.__init__ ( obj )
        
def copy_object ( src, dst ):
    if src != None and dst != None:
        for key in src.__dict__.keys():
            setattr ( dst, key, src.__dict__[key] )
               
    
        