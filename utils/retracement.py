import math

#
#
#

NUM_FIBO_LEVELS = 16

fibolevels = [ 0.05, 0.0903, 0.1458, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 4.235, 6.857, 11.077, 18, 28 ]

#
# Represents the analysis of a quote that can be used to retrieve 
# the retracement levels
#
class QuoteAnalysis(object):
    def __init__( self, numFiboLevels, quotes ):
        self.numfiboLevels = numFiboLevels
        self.quotes = quotes
        
        self.levels = fibolevels
        
        self.transform2()
        
    def transform( self ):             
        self.tbtb = list()
        self.btbt = list()
    
        for (p1,p2,p3,p4) in find_pattern( self.quotes ):
            if p4 != None:
                v1 = (p1 - p2)
                v2 = (p3 - p2)
                theta = math.atan2(v1, v2)

                v3 = (p4 - p3)
                ratio = v3 / v2
                
                fibolevel = quantize_level(self.levels, -ratio)
                
                if p3 > p4:
                    self.tbtb.append((theta, fibolevel))
                else:
                    self.btbt.append((theta, fibolevel))
        self.last_pattern = ( p1, p2, p3, p4 )
        
    def transform2( self ):             
        self.tbtb = list()
        self.btbt = list()
        self.data = list()
    
        for (p1,p2,p3,p4) in find_pattern( self.quotes ):
            if p4 != None:
                v1 = (p1 - p2)
                v2 = (p3 - p2)

                in_ratio = v2 / v1

                v3 = (p4 - p3)
                out_ratio = v3 / v2
                               
                in_level = quantize_level(self.levels, in_ratio)
                out_level = quantize_level(self.levels, -out_ratio)
               
                self.data.append((in_level, out_level))
                if p1 > p2:
                    self.tbtb.append((in_level, out_level))
                else:
                    self.btbt.append((in_level, out_level))
        self.last_pattern = ( p1, p2, p3, p4 )
        
    def get_histogram2(self, p1, p2, p3):
        histogram = [0 for i in range(self.numfiboLevels)]

        v1 = (p1 - p2)
        v2 = (p3 - p2)
        in_ratio = v2 / v1
        in_level = quantize_level(self.levels, in_ratio)

        if p1 > p2:
            data = self.tbtb
        else:
            data = self.btbt
            
     #   data = self.data

        for l in data:
            if l[0] == in_level and l[1] != None:
                histogram[l[1]] += 1

        s = float(sum(histogram))

        if s > 0:
            for i in range(self.numfiboLevels):
                histogram[i] /= s

        return histogram

                    
    def get_histogram(self, p1, p2, p3):
        histogram = [0 for i in range(self.numfiboLevels)]

        v1 = (p1 - p2)
        v2 = (p3 - p2)
        theta = math.atan2(v1, v2)

        if p1 > p2:
            data = self.tbtb
        else:
            data = self.btbt

        for l in data:
            angle = l[0] - theta

            cos = max(math.cos(angle), 0)
            weight = math.pow(cos, 256)
            if l[1] != None:
                histogram[l[1]] += weight

        sum = 0
        for i in range(self.numfiboLevels):
            sum += histogram[i]

        for i in range(self.numfiboLevels):
            histogram[i] /= sum

        return histogram
        
    def get_retracements( self, p1, p2, p3, p4 = None ):
        histogram = self.get_histogram2( p1, p2, p3)
        
        v = ( p3 - p2 )
        
        rl = [ (p3 - v * self.levels[i], 100 * histogram[i]) for i in range(len(self.levels)) ]
    
        return rl
        
    def isGoingLong( self ):
        return self.last_pattern[2] < self.last_pattern[3]


"""
def quantize_level(levels, r):
    
    i = 0
    for l in levels:
        if r > l:
            i = i + 1
        else:
            return i

"""
def quantize_level(levels, r):
    i = 0
    for l in levels:
        if r > l:
            i += 1
        elif i > 0:
            d1 = levels[i-1] - r
            d2 = r - l
            
            if d1 < d2:
                return i
            else:
                return i-1
        else:
            return i

#
#
#
    
def find_pattern( quotes ):    
    state = 0
    i = 0
    
    while i < len(quotes):
        val = quotes[i]
        
        if state == 0:
            p1 = val
            state = 1
            
        elif state == 1:
            p2 = val
            state = 2
                
        elif state == 2:
            if ( p1 < p2 and val < p2 ) or ( p1 > p2 and val > p2 ): 
                p3 = val
                state = 3
            else:
                p2 = val
                
        elif state == 3:
            if ( p2 < p3 and val < p3 ) or ( p2 > p3 and val > p3 ):
                p4 = val
                state = 4
            else:
                p3 = val
                
        elif state == 4:
            if (p3 < p4 and val < p4) or (p3 > p4 and val > p4):
                yield ( p1, p2, p3, p4 )
                   
                p1 = p2
                p2 = p3
                p3 = p4
            p4 = val
        
        i = i + 1

    if state >= 3:
        yield ( p1, p2, p3, val )

def find_last_pattern( quotes ):
    found = False
    
    for ( p1, p2, p3, p4 ) in find_pattern( quotes ):
        found = True
        pass
    
    if found:
        return ( p1, p2, p3, p4 )
    else:
        return None
    

    
    
    
  