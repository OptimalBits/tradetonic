
#
# Trader
#

from retracement import *

MIN_EARNING = 0
MAX_ENTER_ODDS = 30
MIN_EXIT_ODDS = 65

MAX_LONG_ODDS = 10
MAX_SHORT_ODDS = 10

ENTER_TRADE_ODDS = 5
EXIT_TRADE_ODDS = 90

MAX_LOSS = -2
NUM_DAYS = 100

class Trader(object):
    def __init__(self, cash, courtage):
        self.cash = cash
        self.courtage = courtage
        self.stock_price = 0
        self.stock = 0
        self.top_price = 0
        self.bottom_price = 10000000
    
    def buy( self, amount, price ):
        cost = amount * price - self.courtage
        if cost < self.cash:
            self.cash -= amount * price - self.courtage
        else:
            print "NOT ENOUGH MONEY!!"
        
        if self.stock >= 0:
            self.stock_price = ( self.stock_price * self.stock + amount * price ) / ( self.stock + amount )
        
        
        self.stock += amount
        
        print "BOUGHT " + str(amount) + " at " + str(price)
        self.show_info(price)
        
    def sell( self, amount, price ):
        
        self.cash += amount * price - self.courtage
        
        if self.stock <= 0:
            self.stock_price = ( self.stock_price * (-self.stock) + amount * price ) / ( -self.stock + amount )
        
        self.stock -= amount
        
        print "SOLD " + str(amount) + " at " + str(price)         
        self.show_info(price)
        
    def buy_all( self, price ):
        amount = int ( (self.cash - self.courtage) / price)
        self.buy( amount, price )
        
    def sell_all( self, price ):
        self.sell( trader.stock, price )
        
    def short_all( self, price ):
        amount = int ( (self.cash - self.courtage) / price)
        self.sell( amount, price )
        
    def earning( self, current_price ):
        if self.stock_price > 0:
            return calcEarning( self.stock_price, current_price )
        else:
            return 0
        
    def market_value( self, current_price):
        if self.stock > 0:
            return self.stock * current_price
        else:
            return self.cash - (-self.stock) * current_price
      
    def show_info(self, price):
        print  "Amount: " + str(self.stock) + " Cash: " + str(self.cash) + " Price: " + str(self.stock_price) + " Value: " + str(self.market_value( price ))
          
    
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
        
trader = Trader(100000, 100)
        
# Simulate trading.
QUOTE = "../swedbank.txt"
QUOTE = "../lumi.txt"
#QUOTE = "../omx30.txt"
QUOTE = "../volvo b.txt"

input = open(QUOTE, "rb")
lines = input.readlines()
input.close()

quotes = []

for index in range(3,len(lines),8):    
    value = lines[index].strip().replace(',','')
    if len(value) > 0:
        quotes.append(float(value))
        
going_up = False

#quotes = quotes[0:NUM_DAYS]

tbtb = compute_tbtb( quotes )
btbt = compute_btbt( quotes )


# simulate trading
for i in range(NUM_DAYS,0,-1):   
    new_quotes = quotes[:-i]

    tbt = find_last_t1bt2( new_quotes )
    btb = find_last_b1tb2( new_quotes )
    
    if tbt == None and btb == None:
        continue
    
    current_price = new_quotes[-1:][0]
 
    if tbt != None:
        if tbt[2] == current_price:
            if going_up == False:
                reversal = True     
            else:
                reversal = False
            going_up = True
        
    if btb != None:
        if btb[2] == current_price:
            if going_up == True:
                reversal = True
            else:
                reversal = False
            going_up = False
 
    if trader.stock != 0:
        if trader.stock > 0:
            if going_up:
                
                rl = get_retracements( btbt, btb[0], btb[1], btb[2] )
           
                odds = findOdds( current_price, rl )
           
                if odds > MIN_EXIT_ODDS:
                    trader.sell_all( current_price )
                
                 
                trader.top_price = max( trader.top_price, current_price )
            else:
                # Sell if loss > MAX_LOSS from top_price
                earning = calcEarning( trader.top_price, current_price )
                if earning < MAX_LOSS:
                    print "TAKING A LOSS: " + str(earning)
                    trader.sell_all( current_price )
        else:
            if not going_up:
                """
                rl = get_retracements( tbtb, tbt[0], tbt[1], tbt[2] )
                
                odds = findOdds( current_price, rl )
                    
                if odds > MIN_EXIT_ODDS:
                    print "EXIT SHORT TRADE"
                    print "ENTERD LONG TRADE HOPING REVERSAL WITH ODDS: " + str(odds)
                    trader.buy_all( current_price )
                    trader.top_price = current_price
                """
                trader.bottom_price = min( trader.bottom_price, current_price )
            else:
                # Buy if loss > MAX_LOSS from top_price
                earning = calcEarning( current_price, trader.bottom_price )
                if earning < MAX_LOSS:
                    print "TAKING A LOSS: " + str(earning)
                    trader.buy_all( current_price )
                    trader.top_price = current_price
                
    if trader.stock == 0:
        if going_up:
            rl = get_retracements( btbt, btb[0], btb[1], btb[2] ) 
            odds = findOdds( current_price, rl )
                        
            if odds < ENTER_TRADE_ODDS:
                print "ENTER A LONG TRADE WITH ODDS: " + str(odds)
            
                trader.buy_all( current_price )
                trader.top_price = current_price
            
            elif odds > EXIT_TRADE_ODDS:
                print "ENTER A SHORT TRADE HOPING REVERSAL WITH ODDS: " + str(odds)
                trader.short_all( current_price )
                trader.bottom_price = current_price
                 
        elif tbt != None:
           
            rl = get_retracements( tbtb, tbt[0], tbt[1], tbt[2] ) 
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
        
        
        
        
       




