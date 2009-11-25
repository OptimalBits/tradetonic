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

quotes = get_market()

resolution = 'Daily'
histochart = ""

#current_price = quotes[-1:][0]

def embed_svg( svg ):
    return '<script type="image/svg+xml">' + str(svg) + '</script>'
    
def embed_svg2( svg ):
    return '<object data=' + "'data:image/svg+xml," + str(svg) + "'" + 'type="image/svg+xml" width="500" height="500"></object>'

def renderRLChart( quote_id, longReversal = True ):
    
    quote_proxy = QuoteProxy( 'quote_cache' )
    t = quote_proxy.getTicks( quote_id )
   
    q = [ float(r) for r in t.getClosePrices() ]
    
    params = Params()
    
    print q
    
    quote_obj = (i for i in quotes if i.id == quote_id ).next()

    if q[-1] <= q[-2]:
        tbtb = compute_tbtb( q )
        (t1, b, t2 ) = find_last_t1bt2( q ) 
        params.a = t1
        params.b = b
        params.c = t2
    
        rl = get_retracements( tbtb, t1, b, t2 )
        return ( RetracementLevelsChart("", "Odds of reverting to LONG (%)", quote_obj.longName, rl ), params )
        #return ( FibonacciChart( "Just a test", "blabla", q, rl ), params )
    else:
        btbt = compute_btbt( q )
        ( b1, t, b2 ) = find_last_b1tb2( q )
        params.a = b1
        params.b = t
        params.c = b2
        
        rl = get_retracements( btbt, b1, t, b2 )
        
        return ( RetracementLevelsChart("", "Odds of reverting to SHORT (%)", quote_obj.longName, rl ), params )


def update_chart( request, quote_id, longReversal = False ):
    print quote_id

    ( svg, params ) = renderRLChart( quote_id, longReversal )
    return HttpResponse( embed_svg2( svg ) )
    
def update_params( request, quote_id ):
    quote_proxy = QuoteProxy( 'quote_cache' )
    t = quote_proxy.getTicks( quote_id )
   
    q = [ float(r) for r in t.getClosePrices() ]
    
    params = Params()
    
    if q[-1] <= q[-2]:
        (t1, b, t2 ) = find_last_t1bt2( q ) 
        params.a = t1
        params.b = b
        params.c = t2
        
        return render_to_response('tbt.html',{'params':params})
    else:
        ( b1, t, b2 ) = find_last_b1tb2( q )
        params.a = b1
        params.b = t
        params.c = b2
        
        return render_to_response('btb.html',{'params':params})
    
def levels ( request, quote_id = None ):
    if quote_id == None:
        quote_id = quotes[0].id
    
    ( svg, params ) = renderRLChart( quote_id, False )
    histochart = embed_svg2( svg )
    #levelschart = embed_svg2( renderRLChart( quote_id, False ) )
    levelschart = ""
    
    return render_to_response('tradetonic.html', {'quotes': quotes, 'resolution':resolution, 'histochart':histochart, 'levelschart':levelschart, 'params':params } )
    

    

