import math

#
#
#

fibolevels = [ 0.05, 0.0903, 0.1458, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 4.235, 6.857, 11.077, 18, 28 ]


#
# QuoteAnalysisEx
#
# Computes the statistics for V formed patterns, where 
# the number of days is associated to the retracement to some fibonacci level.
#
#
class QuoteAnalysisEx(object):
    def __init__( self, name, fibolevels, quotes ):
        self.levels = fibolevels
        self.quotes = quotes
        self.name = name
        
        self.transform()
        
    # transform data to ( value_level, days_up/down ) tuplets
    def transform():
        self.tbt = list()
        self.btb = list()
       
        ( p1, nd12, p2, nd23, p3 ) = ( None, None, None, None, None )
        for (p1, nd12, p2, nd23, p3) in find_V_pattern( self.quotes ):
            if p4 != None:
                v1 = (p1 - p2)
                v2 = (p3 - p2)

                val_ratio = v2 / v1
                time_ratio = nd23 / nd12
               
                val_level = quantize_level(self.levels, val_ratio)
                time_level = quantize_level(self.levels, time_ratio)
               
                self.data.append((time_level, val_level))
                if p1 > p2:
                    self.tbt.append((time_level, val_level))
                else:
                    self.btb.append((in_level, out_level))
        self.last_pattern = (p1, nd12, p2, nd23, p3)
        
    def get_histogram(self, p1, p2, p3):
        histogram = [0 for i in range(len(self.levels))]

        v1 = (p1 - p2)
        v2 = (p3 - p2)
        val_ratio = v2 / v1
        val_level = quantize_level(self.levels, val_ratio)

        if p1 > p2:
            data = self.tbtb
        else:
            data = self.btbt

        for l in data:
            if l[0] == val_level and l[1] != None:
                histogram[l[1]] += 1

        s = float(sum(histogram))

        if s > 0:
            for i in range(len(self.levels)):
                histogram[i] /= s

        return histogram
        
    def get_retracements( self, p1, p2, p3 = None ):
        if p1 == None or p2 == None:
            return []
        histogram = self.get_histogram( p1, p2, p3)
        
        v = ( p3 - p2 )
        
        rl = [ (p3 - v * self.levels[i], 100 * histogram[i]) for i in range(len(self.levels)) ]
    
        return rl
        
        

#
# Represents the analysis of a quote that can be used to retrieve 
# the retracement levels
#
class QuoteAnalysis(object):
    def __init__( self, name, numFiboLevels, quotes ):
        self.numfiboLevels = numFiboLevels
        self.quotes = quotes
        
        self.levels = fibolevels
        self.name = name
        
        self.transform2()
        
    def transform( self ):             
        self.tbtb = list()
        self.btbt = list()
    
        for (p1,p2,p3,p4,trend) in ( self.quotes ):
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
        self.last_pattern = ( p1, p2, p3, p4, trend )
        
    def transform2( self ):             
        self.tbtb = list()
        self.btbt = list()
        self.data = list()
    
        ( p1, p2, p3, p4, trend ) = ( None, None, None, None, None )
        for (p1,p2,p3,p4,trend) in find_N_pattern( self.quotes ):
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
        self.last_pattern = ( p1, p2, p3, p4, trend )
        
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
        
    def get_retracements( self, p1, p2, p3, p4 = None, trend = None ):
        if p1 == None or p2 == None or p3 == None:
            return []
        histogram = self.get_histogram2( p1, p2, p3)
        
        v = ( p3 - p2 )
        
        rl = [ (p3 - v * self.levels[i], 100 * histogram[i]) for i in range(len(self.levels)) ]
    
        return rl
        
    def get_trend( self ):
        return "{0:.2f}%".format(100 * self.last_pattern[4])
        
    def get_current_odds( self, p1 = None, p2 = None, p3 = None, p4 = None, trend = None ):
        if p1 == None or p2 == None or p3 == None or p4 == None:
            ( p1, p2, p3, p4, trend ) =  self.last_pattern
    
        rls = self.get_retracements( p1, p2, p3, p4 )
        
        if p4 != None:
            last_price = p4
        else:
            if len(self.quotes) >= 1:
                last_price = self.quotes[-1]
            else:
                return 0
        
        odds = []
        sum = 0
        for l in rls:
            if (p2 >= p3 and last_price > l[0]) or (p2 <= p3 and last_price < l[0]):
                sum += l[1]
                odds.append( sum )    
        
        return sum
            
        
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
    
def find_N_pattern( quotes ):    
    state = 0
    i = 0
    
    filtered_quotes = lowPassFilter(quotes, 15)
    
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
                
                d = filtered_quotes[i] - filtered_quotes[i-1]
                theta = math.atan2( d, 1 ) # angle in radians.
                trend = theta / (math.pi/2)
                
                yield ( p1, p2, p3, p4, trend )
                   
                p1 = p2
                p2 = p3
                p3 = p4
            p4 = val
        
        i = i + 1

    if len(filtered_quotes) >= 2:
        d = filtered_quotes[-1] - filtered_quotes[-2]
        theta = math.atan2( d, 1 ) # angle in radians.
        trend = theta / (math.pi/2)
    else:
        trend = 0
                
    if state >= 3:
        yield ( p1, p2, p3, val, trend )

def find_last_pattern( quotes ):
    found = False
    
    for ( p1, p2, p3, p4, trend ) in find_N_pattern( quotes ):
        found = True
        pass
    
    if found:
        return ( p1, p2, p3, p4, trend )
    else:
        return None
  
  
def find_last_pattern2( quotes ):
    found = False
    
    for ( p1, p2, p3, p4 ) in find_N_pattern2( quotes ):
        found = True
        pass
    
    if found:
        return ( p1, p2, p3, p4 )
    else:
        return None      
        
def find_V_pattern( quotes ):    
    state = 0
    i = 0
       
    while i < len(quotes):
        val = quotes[i]
        
        if state == 0:
            p1 = val
            num_days = 0
            state = 1
            
        elif state == 1:
            p2 = val
            state = 2
                
        elif state == 2:
            if ( p1 < p2 and val < p2 ) or ( p1 > p2 and val > p2 ): 
                p3 = val
                num_days_prev = num_days
                state = 3
            else:
                p2 = val
                
        elif state == 3:
            if ( p2 < p3 and val < p3 ) or ( p2 > p3 and val > p3 ):
                
                yield( p1, num_days_prev, p2, num_days, p3 )
            p3 = val
        
        i = i + 1
        num_days = num_days + 1
                
    if state >= 2:
        yield( p1, num_days_prev, p2, num_days, val )
    
    
def rectWeights( supportSize ):
    return [1/float(supportSize)] * supportSize
    
def gaussian( tau, sigma, supportSize ):
    pass
    
def lowPassFilter( data, supportSize ):
    
   # weights = weightFunc( supportSize )
    
    halfSupport = supportSize/2

    out_data = []

    for i in range(len(data)):
        start = max(0, i - halfSupport)
        end = i + halfSupport + 1
        kernel = data[start:end]
        
        d = float(len(kernel))
        if d  > 0:
            s = 1 / d
            out_data.append( sum( x * s for x in kernel ) )
    return out_data
            
def get_bargains( analysis_list ):
    bargains = []
    for a in analysis_list:
        odds = a.get_current_odds( *a.last_pattern )
        trend = a.last_pattern[4]
        if odds > 80:
            if (trend > 0.05) and (a.last_pattern[0] > a.last_pattern[1]):
                bargains.append( (a, 'Buy') )
                print trend
            elif (trend < -0.05) and (a.last_pattern[0] < a.last_pattern[1]):
                bargains.append( (a, 'Sell') )
                print trend
                
    return bargains
    
 
def find_N_pattern2( quotes ):    
    state = 0
    i = 0
      
    while i < len(quotes):
        val = quotes[i]
        
        if state == 0:
            p1 = ( val, i )
            state = 1
            
        elif state == 1:
            p2 = ( val, i )
            state = 2
                
        elif state == 2:
            if ( p1[0] < p2[0] and val < p2[0] ) or ( p1[0] > p2[0] and val > p2[0] ): 
                p3 = ( val, i )
                state = 3
            else:
                p2 = ( val, i )
                
        elif state == 3:
            if ( p2[0] < p3[0] and val < p3[0] ) or ( p2[0] > p3[0] and val > p3[0] ):
                p4 = ( val, i )
                state = 4
            else:
                p3 = ( val, i )
                
        elif state == 4:
            if (p3[0] < p4[0] and val < p4[0]) or (p3[0] > p4[0] and val > p4[0]):                
                yield ( p1, p2, p3, p4 )
                   
                p1 = p2
                p2 = p3
                p3 = p4
            p4 = ( val, i )
        
        i = i + 1
          
    if state >= 3:
        yield ( p1, p2, p3, (val, i) )
    
    
    
    
    
  