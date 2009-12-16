from django.template import Context, loader
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse, NoReverseMatch

from tradetonic.utils import *
from tradetonic.utils.retracementchart import *
from tradetonic.utils.nasdaq_fetcher import *
import datetime

class Params:
    pass

resolution = 'Daily'
histochart = ""

shares = get_market()

def embed_svg( svg ):
    return '<script type="image/svg+xml">' + str(svg) + '</script>'
    
def embed_svg2( svg ):
    return '<object data=' + "'data:image/svg+xml," + str(svg) + "'" + 'type="image/svg+xml" width="500" height="500"></object>'

def renderRLChart( quote_id, resolution = 1 ):
    resolution = int(resolution)
    if resolution >= 1 and resolution < 100:
        quote_proxy = QuoteProxy( 'quote_cache' )
        t = quote_proxy.getTicks( quote_id )
    
        if resolution != 1:
            t = t.samplePrices( resolution )
   
        q = [ float(r) for r in t.getClosePrices() ]
    
        a = QuoteAnalysis(16, q)
        
        going_long = a.isGoingLong()
        
        rl = a.get_retracements( *a.last_pattern )
    
        if not going_long:
            return RetracementLevelsChart("", "Odds of reversing to LONG (%)", "quote_obj.longName", rl )
        else:            
            return RetracementLevelsChart("", "Odds of reversing to SHORT (%)","quote_obj.longName", rl )
    else:
        return "Invalid Parameters!!"
        
        
def renderFiboChart( quote_id, resolution = 1 ):
    
    resolution = int(resolution)
    if resolution >= 1 and resolution < 100:

        quote_proxy = QuoteProxy( 'quote_cache' )
        ticks = quote_proxy.getTicks( quote_id )
   
        if resolution != 1:
            ticks = ticks.samplePrices( resolution )

        q = [ float(r) for r in ticks.getClosePrices() ]
        
        a = QuoteAnalysis(16, q)
        rl = a.get_retracements( *a.last_pattern )
        
        return FibonacciChart( "Fibonacci Levels", "longName", ticks, rl, resolution )
    return HttpResponse("Invalid parameters: " + str(quote_id) + ":" + str(resolution))

def update_chart( request, quote_id, resolution ):
    svg = renderRLChart( quote_id, int(resolution) )
    return HttpResponse( embed_svg2( svg ) )
    
def update_levels( request, quote_id, resolution ):
    svg = renderFiboChart( quote_id, int(resolution) )
    return HttpResponse( embed_svg2( svg ) )
    

# quote_types:
# 1 - Index
# 2 - Shares
def populate_quotes( request, quote_type ):
    if quote_type == 'INDEXES':
        quotes = \
        [ Share('SSESE0000337842', 'SE0000337842', "OMXS30", "OMX Stockholm 30 Index"),
          Share('CSEDX0000001376', 'DX0000001376', "OMXC20", "OMX Copenhagen 20 Index"),
          Share('HEXFI0008900212', 'FI0008900212', "OMXH25", "OMX Helsinki 25 Index"),
          Share('SSESE0001809476', 'SE0001809476', "OMXN40", "OMX Nordic 40 Index"),
        ]

    elif quote_type == 'SHARES':
        quotes = shares
    else:
        quotes = list ()

    return render_to_response('quote_selection.html',{'quotes': quotes})

    
def update_params( request, quote_id, resolution = 1):
    resolution = int(resolution)
    if resolution >= 1 and resolution < 100:
        quote_proxy = QuoteProxy( 'quote_cache' )
        t = quote_proxy.getTicks( quote_id )
    
        if resolution != 1:
            t = t.samplePrices( resolution )
   
        q = [ float(r) for r in t.getClosePrices() ]
       
        params = Params()
   
        ( p1, p2, p3, p4 ) = find_last_pattern( q )
        params.a = p1
        params.b = p2
        params.c = p3
        params.d = q[-1]
        
        if p1 > p2:
            return render_to_response('tbt.html',{'params':params})
        else:
            return render_to_response('btb.html',{'params':params})
    return HttpResponse("Invalid parameters: " + str(quote_id) + ":" + str(resolution))
    
def entry ( request ):    
    return render_to_response('tradetonic.html')
    

    

