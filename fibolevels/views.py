from django.template import Context, loader
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse, NoReverseMatch

from tradetonic.utils import *
from tradetonic.utils.retracementchart import *

quotes = ['Gold', 'OMX PI', 'Volvo AB', 'Swedbank']

selected_quote = 'Volvo AB'

resolution = 'Daily'

input = open("goldprice.txt", "rb")
lines = input.readlines()
input.close()

quotes = []
plot = []
i = 0

#lines.reverse()

for l in lines:
#	date  = l[:10]
	value = l[11:-2]
	quotes.append( float(value) )
	plot.append( (i,float(value)) )	
	i = i + 1

#t1 = 62.15
#b  = 62.10
#t2 = 64.75

#t1 = 60
#b = 50
#t2 = 65

b1 = params_btb[0]
t = params_btb[1]
b2 = params_btb[2]

rl = get_retracements( btbt, b1, t, b2 )
#rl = get_retracements( tbtb, params_tbt[0], params_tbt[1], params_tbt[2] )


histochart = RetracementLevelsChart( "Frequency of SHORT reversals (%)", "Swedbank A", rl )
levelschart = FibonacciChart( "Fibonacci levels", "Gold Bladusir", plot[-1000:], rl )

def levels ( request ):
    return render_to_response('tradetonic.html', {'quotes': quotes, 'selected': selected_quote, 'resolution':resolution, 'histochart':histochart, 'levelschart':levelschart } )
    

