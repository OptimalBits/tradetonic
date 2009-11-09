import math

#
#
#

def get_level(r):

	i = -1
	for l in levels:
		if (r < l):
			i += 1

	return i

#
#
#

def get_histogram(t1, b, t2):

	histogram = []
	for i in range(18):
		histogram.append(0)

	v1 = (t1 - b)
	v2 = (t2 - b)
	theta = math.atan2(v1, v2)

	for l in list:
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
	
	
def get_retracements( t1, b, t2 ):
    histogram = get_histogram(t1, b, t2)
    
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

input = open("goldprice.txt", "rb")
lines = input.readlines()
input.close()

quote = []

for l in lines:
#	date  = l[:10]
	value = l[11:-2]
	quote.append(float(value))

quote.reverse()

#
#
#

levels = []
phi = 0.5*math.sqrt(5) + 0.5

curr = 0.05
for i in range(18):
	levels.append(curr)
	curr *= phi

#
#
#

list = []

#a = quote[i]
b = quote[i+0]
c = quote[i+1]
d = quote[i+2]

for i in range(0, len(quote) - 3):

	a = b
	b = c
	c = d
	d = quote[i+3]

	#
	#	top, bottom, top, bottom
	#

	if (a > b) and (c > b) and (c > d):
		v1 = (a - b)
		v2 = (c - b)
		theta = math.atan2(v1, v2)

		v3 = (d - c)
		ratio = v3 / v2
		list.append([theta, get_level(-ratio)])

#	if (quote[i] < quote[i+1]) and (quote[i+2] < quote[i+1]):
#		print quote[i], quote[i+1], quote[i+2], quote[i+3]
#		foo = foo + 1
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
