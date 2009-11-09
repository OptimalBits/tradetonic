

def str_attr ( attr, val ):
    if val != None:
        return ' ' + attr + '="' + str(val) +  '"'
    else:
        return ''

#class Attribute(object):
#    def __str__ (self):
#        s = ''
#        for k in self.__dict__.keys():
#            s += str_attr ( k,self.__dict__[k] )
#        return s
        
