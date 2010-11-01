#
# Trader
#

from retracement import *
from nasdaq_fetcher import *

MIN_EARNING = 0
MAX_ENTER_ODDS = 30
MIN_EXIT_ODDS = 100

MAX_LONG_ODDS = 10
MAX_SHORT_ODDS = 10

ENTER_TRADE_ODDS = 45
EXIT_TRADE_ODDS = 65

#MAX_LOSS = -0.1
MAX_LOSS = -1
NUM_DAYS = 150

BUY_STOCK = 0
SELL_STOCK = 1

class TradePredictor(object):
    def __init__( self, quotes ):
        #quotes = [ float(r) for r in ticks.getClosePrices() ]
        self.analysis = QuoteAnalysis("", 16, quotes)
    
    def nextTrade( self, odds, quotes ):
        points = find_last_pattern( quotes )
        
        if points == None:
            return None
            
        rl = self.analysis.get_retracements( *points )
    
        return findPrice( odds, rl )
               

class Trader(object):
    def __init__(self, cash, courtage):
        self.cash = cash
        self.courtage = courtage
        self.stock_price = 0
        self.stock = 0
        self.top_price = 0
        self.bottom_price = 10000000
    
    def buy( self, date, amount, price ):
    
        prev_value = self.market_value( self.stock_price )
        
        cost = amount * price + self.courtage
        if cost < self.cash:
            self.cash -= cost
        else:
            print "NOT ENOUGH MONEY!!"
        
        if self.stock >= 0:
            self.stock_price = ( self.stock_price * self.stock + amount * price ) / ( self.stock + amount )
        
        self.stock += amount
        self.stock = int(self.stock)
         
        earning = int(self.market_value( price ) - prev_value)
    
        print date.isoformat() + ": BOUGHT \t" + str(amount) + "\tat " + '%.2f' % price + "\tearning: " + str(earning) + " " + self.info(price)
        
    def sell( self, date, amount, price ):
        		
        prev_value = self.market_value( self.stock_price )
        
        self.cash += amount * price - self.courtage
                        
        if self.stock <= 0:
            self.stock_price = ( self.stock_price * (-self.stock) + amount * price ) / ( -self.stock + amount )
        
        self.stock -= amount
        self.stock = int(self.stock)
        
        earning = int(self.market_value( price ) - prev_value)
        
        print date.isoformat() + ": SOLD   \t" + str(amount) + "\tat " + '%.2f' % price + "\tearning: " + str(earning) + "\t " + self.info(price)
       
    def buy_all( self, date, price ):
        amount = int ( (self.cash - self.courtage) / price)
        self.buy( date, amount, price )
        
    def sell_all( self, date, price ):
        self.sell( date, trader.stock, price )
        
    def short_all( self, date, price ):
        amount = int ( (self.cash - self.courtage) / price) / 0.2
        self.sell( date, amount, price )
        
    def earning( self, current_price ):
        if self.stock_price > 0:
            return calcEarning( self.stock_price, current_price )
        else:
            return 0
        
    def market_value( self, current_price):
        if self.stock > 0:
            return self.stock * current_price + self.cash
        else:
            return self.cash - (-self.stock) * current_price
      
    def show_info(self, price):
        print  self.info( price )
                
    def info(self, price):
        return "Amount: " + str(self.stock) + "\tCash: " + '%.1f' % self.cash + "\tPrice: " + '%.2f' % self.stock_price + "\tValue: " + '%.2f' % self.market_value( price )
          
    
def accumulateOdds( rl ):
    sum = 0
    odds = []
    for l in rl:
        sum += l[1]
        odds.append( sum )
    return odds
    
    
def findOdds( price, rl ):
    odds = accumulateOdds( rl )
        
    for i in range(0, len(odds)-1):
        if (price < rl[i][0]) and (price > rl[i+1][0]):
            d = rl[i][0] - rl[i+1][0]
            t = ( price - rl[i+1][0] ) / d
            
            return t * odds[i] + (1-t)*odds[i+1]
        elif (price > rl[i][0]) and (price < rl[i+1][0]):
            d = rl[i+1][0] - rl[i][0]
            t = ( price - rl[i][0] ) / d
            
            return t * odds[i] + (1-t)*odds[i+1]

    return odds[0]
    
    
def findPrice( odds, rl ):
    odd_list = accumulateOdds( rl )
    
    for i in range( 0, len(odd_list)-1):
        if odd_list[i] <= odds and odd_list[i+1] >= odds:
            t = (odds + odd_list[i]) / ( odd_list[i] + odd_list[i+1] )
            
            price =  rl[i][0] * ( 1 - t ) + rl[i+1][0] * t
            return price
        

def calcEarning( paid_price, sold_price ):
    return ( ( sold_price - paid_price ) / paid_price ) * 100
    
def riskRewardRatio( earning, probability ):
    return  ( probability * earning ) / 100
    
def enterLong( current_price, trader, btbt, params_btb ):
    b1 = params_btb[0]
    t = params_btb[1]
    b2 = params_btb[2]
                
    rl = get_retracements( btbt, b1, t, b2 ) 
    odds = accumulateOdds( rl )
   
    for i in range(0,len(odds)):
        earning = calcEarning( current_price, rl[i][0] )
        if earning > MIN_EARNING:
            if odds[i] < MAX_ENTER_ODDS:
                amount = int (trader.cash / current_price)
                trader.buy( amount, current_price )
                trader.top_price = current_price
            else:
                break
    
def exitLong( current_price, trader, tbtb, params_tbt ):
    t1 = params_tbt[0]
    b = params_tbt[1]
    t2 = params_tbt[2]
                
    rl = get_retracements( tbtb, t1, b, t2 )
    
    odds = accumulateOdds( rl )
   
    # TODO: Sell using money management
    for i in range(0,len(odds)):
        if current_price <= rl[i][0] and odds[i] > MIN_EXIT_ODDS:
            trader.sell( trader.stock, current_price )
            break
                 
def takeLongProfits( current_price, trader ):
    if trader.earning( current_price ) > MAX_EARNING:
        trader.sell( trader.stock, current_price )
    
def enterShort( current_price, trader, tbtb, params_tbt ):
    t1 = params_tbt[0]
    b = params_tbt[1]
    t2 = params_tbt[2]
                
    rl = get_retracements( tbtb, t1, b, t2 )
    
    prices, probs = zip(*rl)
    
    max_prob = max(probs)           
    earning = calcEarning( prices[probs.index(max_prob)], current_price )
    
    if max_prob > MIN_PROB and earning > MIN_EARNING:
        amount = int (trader.cash / current_price)
        trader.sell( amount, current_price )
        trader.bottom_price = current_price
  
def exitShort( current_price, trader, btbt, params_btb ):
    earning = calcEarning( current_price, trader.bottom_price )
  
  #  earning = calcEarning( current_price, trader.stock_price )
  #  if earning > MAX_EARNING:
   #     trader.buy( -trader.stock, current_price )
    if earning < MAX_LOSS:
        trader.buy( -trader.stock, current_price )

def takeShortProfits( current_price, trader ):
    earning = calcEarning( current_price, trader.stock_price )
    if earning > MAX_EARNING:
        trader.buy( -trader.stock, current_price )


# HERE WE START THE SIMULATION
        
trader = Trader(30000, 100)
        
# Simulate trading.
QUOTE = 'SSE101'
QUOTE2 = 'SSE366'
OMXC20 = 'CSEDX0000001376'
OMXS30 = 'SE0000337842'


quote_proxy = QuoteProxy( 'quote_cache' )
ticks = quote_proxy.getTicks( QUOTE2 )

   
quotes = [ float(r) for r in ticks.getClosePrices() ]
dates = ticks.getDates()

#print dates

a = QuoteAnalysis(QUOTE, 16, quotes)
#rl = a.get_retracements( *a.last_pattern )

going_up = False


# simulate trading
"""
for i in range(NUM_DAYS,0,-1):   
    new_quotes = quotes[:-i]
    new_dates = dates[:-i]

    points = find_last_pattern( new_quotes )
    
    if points == None:
        continue
    
    current_price = new_quotes[-1:][0]
    current_date = new_dates[-1:][0]
    
    if points[0] < points[1]:
        if going_up == False:
            reversal = True
        else:
            reversal = False
        going_up = True
            
    if points[0] > points[1]:
        if going_up == True:
            reversal = True
        else:
            reversal = False
        going_up = False
 
    if trader.stock != 0:
        if trader.stock > 0:
            if going_up:
                
                rl = a.get_retracements( *points )
                odds = findOdds( current_price, rl )
           
                if odds > MIN_EXIT_ODDS:
                    trader.sell_all( current_price )
                
                trader.top_price = max( trader.top_price, current_price )
            else:
                # Sell if loss > MAX_LOSS from top_price
                earning = calcEarning( trader.top_price, current_price )
                if earning < MAX_LOSS:
                    #print "TAKING A LOSS: " + str(earning)
                    trader.sell_all( trader.top_price * ( 1 + MAX_LOSS) )
                    #trader.sell_all( current_price )
        else:
            if not going_up:
                
                rl = a.get_retracements( points )
                
                odds = findOdds( current_price, rl )
                    
                if odds > MIN_EXIT_ODDS:
                    print "EXIT SHORT TRADE"
                    print "ENTERED LONG TRADE HOPING REVERSAL WITH ODDS: " + str(odds)
                    trader.buy_all( current_price )
                    trader.top_price = current_price
                
                trader.bottom_price = min( trader.bottom_price, current_price )
            else:
                # Buy if loss > MAX_LOSS from top_price
                earning = calcEarning( current_price, trader.bottom_price )
                if earning < MAX_LOSS:
                    print "TAKING A LOSS: " + str(earning)
                    trader.buy_all( trader.bottom_price * ( 1 + MAX_LOSS) )
                    trader.top_price = current_price
                
    if trader.stock == 0:
        if going_up:
            rl = a.get_retracements( *points ) 
            odds = findOdds( current_price, rl )
                        
            if odds < ENTER_TRADE_ODDS:
                print "ENTER A LONG TRADE WITH ODDS: " + str(odds)
            
                trader.buy_all( current_price )
                trader.top_price = current_price
            
            elif odds > EXIT_TRADE_ODDS:
                print "ENTER A SHORT TRADE HOPING REVERSAL WITH ODDS: " + str(odds)
                trader.short_all( current_price )
                trader.bottom_price = current_price
                 
        elif points != None:
           
            rl = a.get_retracements( *points ) 
            odds = findOdds( current_price, rl )
             
            if odds > EXIT_TRADE_ODDS:
                print "ENTER A LONG TRADE HOPING REVERSAL WITH ODDS: " + str(odds)
            
                trader.buy_all( current_price )
                trader.top_price = current_price
             
            elif odds < ENTER_TRADE_ODDS:
                print "ENTER A SHORT TRADE WITH ODDS: " + str(odds)
            
                trader.short_all( current_price )
                trader.bottom_price = current_price

  
print "Final Amount: " + str(trader.market_value(current_price))
"""        
"""
# simulate trading

for i in range(NUM_DAYS,0,-1):
    new_quotes = quotes[:-i]
    new_dates = dates[:-i]


    points = find_last_pattern( new_quotes )
    
    if points == None:
        continue
    
    current_price = points[3]
    current_date = new_dates[-1:][0]
    
    if points[0] < points[1]:
        if going_up == False:
            reversal = True
        else:
            reversal = False
        going_up = True
            
    if points[0] > points[1]:
        if going_up == True:
            reversal = True
        else:
            reversal = False
        going_up = False
 
    if trader.stock != 0:
        if trader.stock > 0:
            if going_up:  
                rl = a.get_retracements( *points )
                odds = findOdds( current_price, rl )
           
                if odds > MIN_EXIT_ODDS:
                    trader.sell_all( current_date, current_price )
                
                trader.top_price = max( trader.top_price, current_price )
            else:
                # Sell if loss > MAX_LOSS from top_price
                earning = calcEarning( trader.top_price, current_price )
                if earning < MAX_LOSS:
                    #print str(current_date) + ": TAKING A LOSS: " + str(earning)
                    trader.sell_all( current_date, trader.top_price * 0.99 )
        else:
            if not going_up:
                rl = a.get_retracements( *points )
                odds = findOdds( current_price, rl )
                    
                if odds > MIN_EXIT_ODDS:
                    print str(current_date) + ": "
                    #print "EXIT SHORT TRADE"
                    #print "ENTERED LONG TRADE HOPING REVERSAL WITH ODDS: " + str(odds)
                    trader.buy_all( current_date, current_price )
                    trader.top_price = current_price
                
                trader.bottom_price = min( trader.bottom_price, current_price )
            else:
                # Buy if loss > MAX_LOSS from top_price
                earning = calcEarning( current_price, trader.bottom_price )
                if earning < MAX_LOSS:
                    trader.buy_all( current_date, trader.bottom_price * 1.01 )
                    trader.top_price = current_price
                
    if trader.stock == 0:
        if going_up:
            rl = a.get_retracements( *points ) 
            odds = findOdds( current_price, rl )
                        
            if odds < ENTER_TRADE_ODDS:
                #print str(current_date) + ": ENTER A LONG TRADE WITH ODDS: " + str(odds)
            
                trader.buy_all( current_date, current_price )
                trader.top_price = current_price
         #    
            elif odds > EXIT_TRADE_ODDS:
                #print str(current_date) + ": ENTER A SHORT TRADE HOPING REVERSAL WITH ODDS: " + str(odds)
                trader.short_all( current_date, current_price )
                trader.bottom_price = current_price
          #  
        elif points != None:
           
            rl = a.get_retracements( *points ) 
            odds = findOdds( current_price, rl )
          #  
            if odds > EXIT_TRADE_ODDS:
                #print str(current_date) + ": ENTER A LONG TRADE HOPING REVERSAL WITH ODDS: " + str(odds)           
                trader.buy_all( current_price )
                trader.top_price = current_price
           # 
            if odds < ENTER_TRADE_ODDS:
                #print str(current_date) + ": ENTER A SHORT TRADE WITH ODDS: " + str(odds)
            
                trader.short_all( current_date, current_price )
                trader.bottom_price = current_price
"""
    
    
#predictor = TradePredictor( ticks )
show_indicator = True

# simulate trading
for i in range(NUM_DAYS,-1,-1):
    if i > 0:
        new_quotes = quotes[:-i]
        new_dates = dates[:-i]
    else:
        new_quotes = quotes
        new_dates = dates

    predictor = TradePredictor( new_quotes )
    current_date = new_dates[-1:][0]
    
    tick = ticks[current_date]
    print tick
    
    new_quotes = new_quotes[:-1]
    points = find_last_pattern( new_quotes )
    
    if points == None:
        continue
   
    if points[0] < points[1]:
        if going_up == False:
            reversal = True
        else:
            reversal = False
        going_up = True
            
    if points[0] > points[1]:
        if going_up == True:
            reversal = True
        else:
            reversal = False
        going_up = False
        
    price_enter = predictor.nextTrade( ENTER_TRADE_ODDS, new_quotes )
    price_exit = predictor.nextTrade( EXIT_TRADE_ODDS, new_quotes )
    
    min_price = min( price_enter, price_exit )
    max_price = max( price_enter, price_exit )
        
    if show_indicator:
        if price_enter != None:
            print "Next buying price: " + '%.2f' % min_price
        
        if price_exit != None:
            print "Next sell price: " + '%.2f' % max_price
        
    low = tick.low
    high = tick.high
 
    if trader.stock != 0:
        if trader.stock > 0:
            if going_up:     
          #      if price <= current_price:
          #          trader.sell_all( current_date, current_price )
                
                trader.top_price = max( trader.top_price, high )
            else:
                earning = calcEarning( trader.top_price, low )
                
                if earning < MAX_LOSS:
                    sell_price = min( trader.top_price * 0.99, high )
                    trader.sell_all( current_date, sell_price )
        else:
            if not going_up:  
          #      if price >= current_price:  
          #          trader.buy_all( current_date, current_price )
          #          trader.top_price = current_price
                
                trader.bottom_price = min( trader.bottom_price, low )
            else:
                earning = calcEarning( high, trader.bottom_price )
                
                if earning < MAX_LOSS:
                    buy_price = max( trader.bottom_price * 1.01, low )
                    trader.buy_all( current_date, buy_price )
                    trader.top_price = buy_price
                
    if trader.stock == 0:
        
        if going_up:
            if low <= max_price <= high:
                trader.short_all( current_date, max_price )
                trader.bottom_price = max_price    
            elif low <= min_price <= high:
                trader.buy_all( current_date, min_price )
                trader.top_price = min_price
        else:
            if low <= min_price <= high:
                trader.buy_all( current_date, min_price )
                trader.top_price = min_price
            elif low <= max_price <= high:
                trader.short_all( current_date, max_price )
                trader.bottom_price = max_price
            
       
       
        #if current_price >= max_price:
        #    trader.short_all( current_date, current_price )
        #    trader.bottom_price = current_price    
        #elif current_price <= min_price:
        #    trader.buy_all( current_date, current_price )
        #    trader.top_price = current_price
       
        
    #    if going_up:                 
     #       if price_enter >= current_price:
      #          trader.buy_all( current_date, current_price )
       #         trader.top_price = current_price
            
        #    elif price_exit <= current_price:
         #       trader.short_all( current_date, current_price )
          #      trader.bottom_price = current_price
        #elif points != None:
         #   if price_exit <= current_price:
          #      trader.short_all( current_date, current_price )
           #     trader.bottom_price = current_price
            
           # elif price_enter >= current_price:
            #    trader.buy_all( current_date, current_price )
             #   trader.top_price = current_price
                
            #if price_exit <= current_price:            
            #    trader.short_all( current_date, current_price )
            #    trader.bottom_price = current_price

price_enter = predictor.nextTrade( ENTER_TRADE_ODDS, quotes )
price_exit = predictor.nextTrade( EXIT_TRADE_ODDS, quotes )
    
min_price = min( price_enter, price_exit )
max_price = max( price_enter, price_exit )
        
if show_indicator:
    print "Next buying price: " + '%.2f' % min_price
    print "Next sell price: " + '%.2f' % max_price









