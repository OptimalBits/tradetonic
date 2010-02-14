from django.template import Context, loader
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse, NoReverseMatch

from tradetonic.tabmenu.models import *
from tradetonic.utils import *
from tradetonic.utils.retracementchart import *
from tradetonic.utils.nasdaq_fetcher import *
import datetime

class Params:
    pass

resolution = 'Daily'
histochart = ""

shares = get_market()
indexes = \
        [ Share('SSESE0000337842', 'SE0000337842', "OMXS30", "OMX Stockholm 30 Index"),
          Share('CSEDX0000001376', 'DX0000001376', "OMXC20", "OMX Copenhagen 20 Index"),
          Share('HEXFI0008900212', 'FI0008900212', "OMXH25", "OMX Helsinki 25 Index"),
          Share('SSESE0001809476', 'SE0001809476', "OMXN40", "OMX Nordic 40 Index"),
        ]
        
def find_name( quote_id, quotes ):
    for q in quotes:
        if quote_id == q.id:
            return q

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
    
        longName = find_name( quote_id, shares + indexes ).longName
        a = QuoteAnalysis( longName, 16, q)
        
        going_long = a.isGoingLong()
        
        rl = a.get_retracements( *a.last_pattern )
    
        if not going_long:
            return RetracementLevelsChart("", "Odds of reversing to LONG (%)", a.name, rl )
        else:            
            return RetracementLevelsChart("", "Odds of reversing to SHORT (%)", a.name, rl )
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
        
        longName = find_name( quote_id, shares + indexes ).longName
        a = QuoteAnalysis(longName, 16, q)
        rl = a.get_retracements( *a.last_pattern )
        
        return FibonacciChart( "Fibonacci Levels", a.name, ticks, rl, resolution )
    return HttpResponse("Invalid parameters: " + str(quote_id) + ":" + str(resolution))

def update_chart( request, quote_id, resolution, tabs ):
    svg = renderRLChart( quote_id, int(resolution) )
    return HttpResponse( embed_svg2( svg ) )
    
def update_levels( request, quote_id, resolution, tabs ):
    svg = renderFiboChart( quote_id, int(resolution) )
    return HttpResponse( embed_svg2( svg ) )
    

# quote_types:
# 1 - Index
# 2 - Shares
def populate_quotes( request, quote_type, tabs ):
    if quote_type == 'INDEXES':
        quotes = indexes
    elif quote_type == 'SHARES':
        quotes = shares
    else:
        quotes = list ()

    return render_to_response('quote_selection.html',{'quotes': quotes})

    
def update_params( request, quote_id, resolution = 1, tabs = None):
    resolution = int(resolution)
    if resolution >= 1 and resolution < 100:
        quote_proxy = QuoteProxy( 'quote_cache' )
        t = quote_proxy.getTicks( quote_id )
    
        if resolution != 1:
            t = t.samplePrices( resolution )
   
        q = [ float(r) for r in t.getClosePrices() ]
       
        params = Params()
   
        ( p1, p2, p3, p4, trend ) = find_last_pattern( q )
        params.a = p1
        params.b = p2
        params.c = p3
        params.d = q[-1]
        trend =  round( trend * 100, 2 )
        if trend > 0:
            params.trend = "{0:.2f}".format(trend) + "% ( bullish )"
        else:
            params.trend = str(trend) + "% ( bearish )"
        
        a = QuoteAnalysis("", 16, q)
        
        params.odds = "{0:.2f}%".format(a.get_current_odds( p1, p2, p3, p4 ))
        
        return render_to_response('params.html',{'params':params, 'up_trend':p2 > p1})
        
    return HttpResponse("Invalid parameters: " + str(quote_id) + ":" + str(resolution))
    
def show_charts ( request, tabs ):
    t = select_tab( tabs, "Fibonacci Levels" )
    select_tab( t.subtabs, "Chart" )
    return render_to_response('fibolevels.html',{'tabs':tabs})
    

def show_bargains ( request, tabs ):
    t = select_tab( tabs, "Fibonacci Levels" )
    select_tab( t.subtabs, "Bargains" )
    
    # analyze all shares ( TODO: Implement caching here ).
    cache = QuoteCache('bargains_cache')
    analysis = cache.query( str(datetime.date.today()) )
    if analysis == None:
        analysis = []
        for s in shares:
            quote_proxy = QuoteProxy( 'quote_cache' )
            t = quote_proxy.getTicks( s.id )
   
            q = [ float(r) for r in t.getClosePrices() ]
            a = QuoteAnalysis( s.longName, 16, q)
            a.odds = "{0:.2f}%".format( a.get_current_odds() )
            analysis.append( a )
        cache.put( str(datetime.date.today()), analysis )
    
    share_list = get_bargains( analysis )
    
    return render_to_response('bargains.html',{'tabs':tabs,'share_list':share_list})
    
    

