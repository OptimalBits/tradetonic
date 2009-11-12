import math

#
#
#


def get_fibonacci_level(levels, r):
    
    i = 0
    for l in levels:
        if r > l:
            i = i + 1
        else:
            return i

def get_level(levels, r):
    i = -1
    for l in levels:
        if (r < l):
            i += 1
                   
    return i

#
#
#

def get_histogram(tbtb, t1, b, t2):
    histogram = [0 for i in range(18)]

    v1 = (t1 - b)
    v2 = (t2 - b)
    theta = math.atan2(v1, v2)

    for l in tbtb:
        angle = l[0] - theta

        cos = max(math.cos(angle), 0)
        weight = math.pow(cos, 256)
        histogram[l[1]] += weight

    sum = 0
    for i in range(18):
        sum += histogram[i]

    for i in range(18):
        histogram[i] /= sum

    return histogram
	
	
def get_retracements( tbtb, t1, b, t2 ):
    histogram = get_histogram(tbtb, t1, b, t2)
    
    levels = []
    phi = 0.5*math.sqrt(5) + 0.5

    curr = 0.05
    for i in range(len(histogram)):
	   levels.append(curr)
	   curr *= phi
    
    rl = []
    for i in range(len(levels)):
	   rl.append( (t2 - (t2 - b) * levels[i], 100*histogram[i] ) )

    return rl

#
#
#

def compute_tbtb_old( quotes ):
    levels = []
    phi = 0.5*math.sqrt(5) + 0.5

    curr = 0.05
    for i in range(18):
        levels.append(curr)
        curr *= phi
        
    tbtb = list()

    b = quotes[0]
    c = quotes[1]
    d = quotes[2]

    for i in range(0, len(quotes) - 3):
        a = b
        b = c
        c = d
        d = quotes[i+3]

	   #
	   #	top, bottom, top, bottom
	   #

        if (a > b) and (c > b) and (c > d):
            v1 = (a - b)
            v2 = (c - b)
            theta = math.atan2(v1, v2)

            v3 = (d - c)
            ratio = v3 / v2
            tbtb.append([theta, get_level(levels, -ratio)])
            
    return tbtb 
    

def compute_tbtb( quotes ):
    levels = []
    phi = 0.5*math.sqrt(5) + 0.5

    curr = 0.05
    for i in range(18):
        levels.append(curr)
        curr *= phi
        
    tbtb = list()
    
    state = 0
    i = 0
    
    while i < len(quotes):
        val = quotes[i]
        
        if state == 0:
            t1 = val
            state = 1
        elif state == 1:
            if val < t1:
                b1 = val
                state = 2
            else:
                t1 = val    
        elif state == 2:
            if val > b1:
                t2 = val
                state = 3
            else:
                b1 = val
        elif state == 3:
            if val < t2:
                b2 = val
                state = 4
            else:
                t2 = val
        elif state == 4:
            if val > b2:
                v1 = (t1 - b1)
                v2 = (t2 - b1)
                theta = math.atan2(v1, v2)

                v3 = (b2 - t2)
                ratio = v3 / v2
                fibolevel = get_fibonacci_level(levels, -ratio)
                tbtb.append((theta, fibolevel))
                
                t1 = t2
                b1 = b2
                t2 = val
                state = 3
            else:
                b2 = val
        
        i = i + 1
             
    return ( (t1,b1,t2), tbtb ) 

def compute_btbt( quotes ):
    levels = []
    phi = 0.5*math.sqrt(5) + 0.5

    curr = 0.05
    for i in range(18):
        levels.append(curr)
        curr *= phi

    btbt = list()
    
    state = 0
    i = 0
    
    while i < len(quotes):
        val = quotes[i]
        
        if state == 0:
            b1 = val
            state = 1
        elif state == 1:
            if val > b1:
                t1 = val
                state = 2
            else:
                b1 = val    
        elif state == 2:
            if val < t1:
                b2 = val
                state = 3
            else:
                t1 = val
        elif state == 3:
            if val > b2:
                t2 = val
                state = 4
            else:
                b2 = val
        elif state == 4:
            if val < t2:
                v1 = (b1 - t1)
                v2 = (b2 - t1)
                theta = math.atan2(v1, v2)

                v3 = (t2 - b2)
                ratio = v3 / v2
                fibolevel = get_fibonacci_level(levels, -ratio)
                btbt.append((theta, fibolevel))
                 
                b1 = b2
                t1 = t2
                b2 = val
                state = 3
            else:
                t2 = val
        
        i = i + 1
                    
    return ( (b1, t1, b2), btbt )
    
#
#
#

# Read gold stuff
input = open("goldprice.txt", "rb")
lines = input.readlines()
input.close()

quotes = []

for l in lines:
#	date  = l[:10]
	value = l[11:-2]
	quotes.append(float(value))

quotes.reverse()

# read swedbank
"""
input = open("swedbank.txt", "rb")
lines = input.readlines()
input.close()

quotes = []

for l in lines:
#	date  = l[:10]
	value = l[11:-2]
	quotes.append(float(value))

quotes.reverse()
"""

#   


"""
t1 = 1360.03
b  = 1342.53
t2 = 1353.11
histogram = get_histogram(t1, b, t2)

sum = 0
for i in range(18):
	sum += histogram[i]
	print "%.2f: %.2f%%\t(%.2f%%)" %(t2 - (t2 - b) * levels[i], 100*histogram[i], 100*sum)


print get_retracements( t1, b, t2 )

print levels
   """ 
