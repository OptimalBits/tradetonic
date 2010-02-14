
from nasdaq_fetcher import *
from retracement import *
import datetime

d = str(datetime.date.today())

print "Pre fetching and pre processing stock data ..."
print "Date: \s", d

shares = get_market()

cache = QuoteCache('../bargains_cache')
quote_proxy = QuoteProxy( '../quote_cache' )

analysis = cache.query( d )
    
if ( analysis == None )  or ( len(analysis) == 0 ):
     analysis = []
     for s in shares:
        print "processing %s ...", s.longName
        t = quote_proxy.getTicks( s.id )
        q = [ float(r) for r in t.getClosePrices() ]
        a = QuoteAnalysis( s.longName, 16, q)
        a.odds = "{0:.2f}%".format( a.get_current_odds() )
        print a.odds
        analysis.append( a )    
     cache.put( d, analysis )
    
    


