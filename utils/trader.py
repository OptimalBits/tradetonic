
#
# Trader
#

from retracement import *

MIN_EARNING = 1.5
MAX_ODDS = 40

MAX_LOSS = -1.5
NUM_DAYS = 350

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
        print  "Amount: " + str(self.stock) + " Cash: " + str(self.cash) + "Price: " + str(self.stock_price) + " Value: " + str(self.market_value( price ))
          
    
def accumulateOdds( rl ):
    sum = 0
    odds = []
    for l in rl:
        sum += l[1]
        odds.append( sum )
    return odds
        

def calcEarning( paid_price, sold_price ):
    #print str(paid_price) + ":" + str(sold_price)
    return ( ( sold_price - paid_price ) / paid_price ) * 100
    
# risk = 1 - ProbabilityRetracement
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
            if odds[i] < MAX_ODDS:
                amount = int (trader.cash / current_price)
                trader.buy( amount, current_price )
                trader.top_price = current_price
                
            else:
                break
    """
    prices, probs = zip(*rl)
    
    max_prob = max(probs)           
    earning = calcEarning( current_price, prices[probs.index(max_prob)])
    
    if max_prob > MIN_PROB and earning > MIN_EARNING:
        amount = int (trader.cash / current_price)
        trader.buy( amount, current_price )
        trader.top_price = current_price
    """
    
def exitLong( current_price, trader, tbtb, params_tbt ):
    earning = calcEarning( trader.top_price, current_price )

    if earning < MAX_LOSS:
         trader.sell( trader.stock, current_price )
        
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

input = open("swedbank.txt", "rb")
lines = input.readlines()
input.close()

quotes = []

for index in range(3,len(lines),8):    
    value = lines[index].strip()
    if len(value) > 0:
        quotes.append(float(value))
        
going_up = False

a = compute_tbtb( quotes )
tbtb = a[1]

b = compute_btbt( quotes )
btbt = b[1]

# simulate trading
for i in range(NUM_DAYS,0,-1):   
    new_quotes = quotes[:-i]

    a = compute_tbtb( new_quotes )
    # tbtb = a[1]
    params_tbt = a[0] 

    b = compute_btbt( new_quotes )
    # btbt = b[1]
    params_btb = b[0]
      
    current_price = new_quotes[-1:][0]
 
    if params_tbt[2] == current_price:
        # Go long
        if going_up == False:
            reversal = True     
        else:
            reversal = False
        going_up = True
        
    elif params_btb[2] == current_price:
        # Go Short
        if going_up == True:
            reversal = True
        else:
            reversal = False
        going_up = False
               
    else:
        print "SOMETHING WRONG!!"

    if trader.stock != 0:
        if reversal:
            if trader.stock > 0:
                #print "EXITING LONG..."
                exitLong( current_price, trader, tbtb, params_tbt )
            else:
                #print "EXITING SHORT..."
                exitShort( current_price, trader, btbt, params_btb )
                pass
        else:
            trader.top_price = max( trader.top_price, current_price )
            trader.bottom_price = min( trader.bottom_price, current_price )
           # if trader.stock > 0:
           #     takeLongProfits( current_price, trader )
           # else:
           #     takeShortProfits(current_price, trader )
  
    if trader.stock == 0:
        if reversal:
            if going_up:
                #print "ENTERING LONG..."
                enterLong( current_price, trader, btbt, params_btb )
            else:
                #print "ENTERING SHORT..."
                #enterShort( current_price, trader, tbtb, params_tbt )
                pass
        else:
            pass # Wait for proper market conditions
            
   
  
print "Final Amount: " + str(trader.market_value(current_price))
        
        
        
        
       




