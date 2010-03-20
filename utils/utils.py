
import inspect


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
   
def init_bases ( cls, obj, **kwargs ):
    for attr in inspect.getmro( cls )[1:]:
        if inspect.ismethod(attr.__init__):
            validargs = getValidArgs( attr.__init__, kwargs )
            attr.__init__ ( obj, **validargs )
           
def copy_object ( src, dst ):
    if src != None and dst != None:
        for key in src.__dict__.keys():
            setattr ( dst, key, src.__dict__[key] )
            
def getValidArgs(func, argsDict):
    '''Return dictionary without invalid function arguments.'''
    validArgs = func.im_func.func_code.co_varnames[:func.func_code.co_argcount]
    return dict((key, value) for key, value in argsDict.iteritems() 
                if key in validArgs)
    
def invalidArgs(func, argdict):
    args, varargs, varkw, defaults = getargspec(func)
    if varkw: return set()  # All accepted
    return set(argdict) - set(args)
    
    
        