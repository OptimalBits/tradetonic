"""
OMX NASDAQ NORDIQ DATA FETCHER:

xmlquery	
<post> 
<param name="SubSystem" value="History"/> 
<param name="Action" value="GetDataSeries"/> 
<param name="AppendIntraDay" value="no"/> 
<param name="Instrument" value="SSE366"/> 
<param name="FromDate" value="2009-10-20"/> 
<param name="ToDate" value="2009-11-20"/> 
<param name="hi__a" value="0,1,2,4,21,8,10,11,12,9"/> 
<param name="ext_xslt" value="test/hi_table.xsl"/> 
<param name="ext_xslt_options" value=",unadjusted,"/> 
<param name="ext_xslt_lang" value="en"/> 
<param name="ext_xslt_hiddenattrs" value=",ip,iv,"/> 
<param name="ext_xslt_tableId" value="historicalTable"/> 
</post>
"""

"""
# Shares
xmlquery	
<post> 
<param name="Exchange" value="NMF"/> 
<param name="SubSystem" value="Prices"/> 
<param name="Action" value="GetMarket"/> 
<param name="inst__a"value="0,87,1,2,5,37,4,20,21,23,24,33,34,97,129,98,72"/> 
<param name="ext_xslt" value="inst_table.xsl"/> 
<param name="Market" value="L:3303"/> 
<param name="inst__e" value="7"/> 
<param name="instrumentType" value="S"/> 
<param name="ext_xslt_sortattribute" value="fnm"/> 
<param name="ext_xslt_lang" value="en"/> 
<param name="ext_xslt_tableId" value="searchSharesListTable"/> 
<param name="ext_xslt_hiddenattrs" value=",lists,tp,hlp,isin,note,mktc,"/> <param name="ext_xslt_tableClass" value="tablesorter"/> 
<param name="ext_xslt_options" value=",noflag,sectoridicon,truncate,mylist,"/> 
</post>
"""

"""
# Index
<post> 
<param name="Exchange" value="NMF"/> 
<param name="SubSystem" value="Prices"/> 
<param name="Action" value="GetMarket"/> <param name="inst__a" value="0,1,2,21,35,36,109,110"/> 
<param name="ext_xslt" value="inst_table.xsl"/> 
<param name="Market" value="IndexX:1"/> 
<param name="XPath" value="//inst[starts-with(@nm,'OMXN') or starts-with(@nm,'N')]"/> <param name="ext_xslt_lang" value="en"/> <param name="ext_xslt_tableId" value="searchNordicIndexesTable"/> <param name="ext_xslt_tableClass" value="tablesorter"/> <param name="ext_xslt_options" value=",noflag,"/> 
</post>
"""

"""
<post> 
<param name="SubSystem" value="Prices"/> 
<param name="Action" value="GetInstrument"/> 
<param name="inst__a" value="1,2,37,20,21"/> 
<param name="Exception" value="false"/> 
<param name="ext_xslt" value="inst_table.xsl"/> <param name="Instrument" value="SSESE0001809476"/> <param name="Instrument" value="CSEDX0000001376"/> <param name="Instrument" value="SSESE0000337842"/> <param name="Instrument" value="HEXFI0008900212"/> <param name="Instrument" value="ICEIS0000018885"/> <param name="ext_xslt_lang" value="en"/> <param name="ext_xslt_tableId" value="nordicIndexesGraphTable"/> <param name="ext_xslt_options" value=",noflag,nozebra,"/> </post>
"""
"""
<post> 
<param name="SubSystem" value="Prices"/> 
<param name="Action" value="GetInstrument"/> 
<param name="inst__a" value="1,2,37,34,20,21,35,36,10"/> 
<param name="Exception" value="false"/> 
<param name="ext_xslt" value="inst_table.xsl"/> 
<param name="Instrument" value="SSESE0000337842"/> 
<param name="ext_xslt_lang" value="en"/> 
<param name="ext_xslt_tableId" value="avistaTable"/> 
<param name="ext_xslt_options" value=",noflag,nolink,"/> 
</post>

<post> 
<param name="SubSystem" value="History"/> 
<param name="Action" value="GetDataSeries"/> 
<param name="AppendIntraDay" value="no"/> 
<param name="Instrument" value="SSESE0000337842"/> 
<param name="FromDate" value="2009-09-02"/> 
<param name="ToDate" value="2009-12-02"/> 
<param name="hi__a" value="0,1,2,4,21,8,10,11,12"/> 
<param name="ext_xslt" value="hi_table.xsl"/> 
<param name="ext_xslt_lang" value="en"/> 
<param name="ext_xslt_hiddenattrs" value=",ip,iv,"/> 
<param name="ext_xslt_tableId" value="historicalTable"/> 
</post>
"""

import os
import os.path
import cPickle
import xml.parsers.expat

class QuoteDayTick(object):
    def __init__(self, date, low, high, close, volume):
        self.date = strToDate(date)
        if low == '':
            low = 0
            
        if high == '':
            high = 0
            
        if close == '':
            close = 0
            
        if volume == '':
            volume = 0
        
        self.low = float(low)
        self.high = float(high)
        self.close = float(close)
        self.volume = float(volume)
            
    def __str__(self):
        s = str(self.date) + " low: " 
        s+= str(self.low)  + " high: " 
        s+= str(self.high) + " close: " 
        s+= str(self.close) + " vol.: " 
        s+= str(self.volume) 
        return s
        
        
        
            
class QuoteList(dict):
    def getClosePrices(self, startDate = None, endDate = None):
        quotes_list = self.items()
        quotes_list.sort()
        if startDate != None and endDate == None:
            return [q.close for (d,q) in quotes_list if d >= startDate]
        elif startDate == None and endDate != None:
            return [q.close for (d,q) in quotes_list if d <= endDate]
        elif startDate != None and endDate != None:
            return [q.close for (d,q) in quotes_list if d >= startDate and d <= endDate ]
        else:
            return [q.close for (d,q) in quotes_list]
            
    def getDates( self ):
        quotes_list = self.items()
        quotes_list.sort()
        return [q.date for (d,q) in quotes_list]
            
    # Sample prices
    # Approximate a week with 5 days.
    # Approximate a month with 20 days
    def samplePrices(self, resolution ):
        sampled_quotes = QuoteList()
        quotes_list = self.items()
        quotes_list.sort()
        
        # Very simple Point sampling:
        for i in range(0, len(quotes_list), resolution):
            (d,q) = quotes_list[i]
            sampled_quotes[d] = q
            
        return sampled_quotes
        
        
    def __str__(self):
        s = ""
        for q in self:
            s += str(q) + "\n"
        return s

class QuoteCache(object):    
    def __init__(self, directory):
        self.directory = directory
        if not os.path.exists( directory ):
            os.mkdir( directory )
            
    def query( self, id ):
        
        if os.path.exists( self.cachedFilename(id) ):
            f = open( self.cachedFilename(id), 'r')
            quotes = cPickle.load( f )
            return quotes
        else:
            return None
        
    def put( self, id, quote_list ):
        #if len(quote_list) > 0: 
            if not os.path.exists( self.cachedFilename(id) ):
                f = open( self.cachedFilename(id), 'w')
                cPickle.dump( quote_list, f )
        
    def cachedFilename( self, id ):
        return os.path.join(self.directory, id + '_' + str(datetime.date.today()) ) 
        
 
           
class QuoteProxy(object):
    def __init__(self, directory):
        self.cache = QuoteCache( directory )
        
    def getTicks( self, id ):

        quotes = self.cache.query( id )
        if quotes != None:
            return quotes
        else:
            quotes = get_ticks( id, strToDate('1970-10-01') )
            self.cache.put( id, quotes ) 
            return quotes
           

import datetime

class Share(object):
    def __init__( self, id, isin, shortName, longName ):
        self.id = id
        self.isin = isin
        self.shortName = shortName
        self.longName = longName

    def __str__(self):
        s = unicode(self.shortName) + u", "
        s+= unicode(self.longName) + u", " 
        s+= unicode(self.isin) + u", " 
        s+= unicode(self.id) 
        return s

        
class ShareList(list):
        
    def __str__(self):
        s = unicode()
        for q in self:
            s += unicode(q) + "\n"
        return s
        
class ShareCache(object):
    def __init__(self, directory):
        pass

def get_market():
    params_dict = { 'Exchange':'NMF', 'SubSystem':'Prices', 'Action':'GetMarket', 'Market':'L:10214', 'instrumentType':'S' }
    
    import urllib
    params = urllib.urlencode(params_dict)
    
    shares = ShareList()

    f = urllib.urlopen("http://www.nasdaqomxnordic.com/webproxy/DataFeedProxy.aspx?%s" % params)

    print "http://www.nasdaqomxnordic.com/webproxy/DataFeedProxy.aspx?%s" % params
    
    def start_element(name, attrs):
        if name == 'inst':
            shares.append( Share( attrs['id'], attrs['isin'], attrs['nm'], attrs['fnm'] ) )
            
    p = xml.parsers.expat.ParserCreate()

    p.StartElementHandler = start_element
   
    p.Parse(f.read())

    return shares
    
def get_ticks( instrumentId, fromDate = datetime.date.today(), toDate = datetime.date.today() ):
    params_dict = { 'SubSystem':'History', 'Action':'GetDataSeries', 'Instrument': 'SSE366', "AppendIntraDay":"no", "FromDate":"2009-10-20", "ToDate":"2009-11-20" }
    
    params_dict['Instrument'] = instrumentId
    params_dict['FromDate'] = str(fromDate)
    params_dict['ToDate'] = str(toDate)
    
    import urllib
    params = urllib.urlencode(params_dict)

    f = urllib.urlopen("http://www.nasdaqomxnordic.com/webproxy/DataFeedProxy.aspx?%s" % params)
  
    
    quotes = QuoteList()

    # 3 handler functions
    def start_element(name, attrs):
         if name == 'hi':
            if attrs['cp'] != '':
                q = QuoteDayTick( attrs['dt'], attrs['lp'], attrs['hp'], attrs['cp'], attrs['tv'] )
                quotes[q.date] = q
    def end_element(name):
        pass
    def char_data(data):
        print 'Character data:', repr(data)

    p = xml.parsers.expat.ParserCreate()

    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.CharacterDataHandler = char_data

    p.Parse(f.read())
    
    return quotes
   
def strToDate( date ):
    return datetime.date( int(date[0:4]), int(date[5:7]), int(date[8:]) )

    







