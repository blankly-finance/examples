import requests
import json
import blankly
import datetime
from os.path import exists

def time_utility(time):
  return datetime.datetime.strptime(time, '%Y-%m-%d')

def init(symbols, state: blankly.StrategyState):
    # Download past price data for initialization.
    state.variables['history'] = {symbol:state.interface.history(symbol, to=50, return_as='list',
                                                         resolution=state.resolution)['close'] for symbol in symbols}
    '''
    Store earnings dates for each ticker in a dictionary of lists.
    Each ticker maps to a sequential list of earnings dates.
    '''
    state.earnings_dates = {}
    '''Use the Financial Modeling Prep API to pull earnings dates and store them in .json files.
    Store the files in a local folder
    If we have already downloaded said data, skip over the ticker.
    '''
    for symbol in symbols:
      if not exists('CalendarJSONs/'+symbol + '.json'):
        result = requests.get('https://financialmodelingprep.com/api/v3/historical/earning_calendar/'+symbol+'?apikey=YOUR_API_KEY')
        data = result.json()
        with open('CalendarJSONs/'+symbol+'.json', 'w+') as f:
          json.dump(data, f)
      with open('CalendarJSONs/'+symbol+'.json', 'r') as f:
          rdata = json.load(f)
      '''
      Initialize an empty list to store earnings dates.
      Store dates from least recent to most recent.
      '''
      lis = []
      for elem in rdata[::-1]:
          lis.append(time_utility(elem['date']))
      state.earnings_dates[symbol] = lis

    # Helper data that we will store to encode where we are in the list of earnings dates 
    state.earnings_indices = {symbol:0 for symbol in symbols}

    #Dictionary -- track which securities we own positions in
    state.variables['owns_position'] = {symbol:False for symbol in symbols}

    '''Have we initialized earnings indices yet?
    We have to do this in the first iteration of our arbitrage event
    because our starting point is dependent on the backtest length
    '''
    state.variables['init_indices'] = False

def earn_event(prices, symbols, state: blankly.StrategyState):
  '''
  We use the last element in symbols as the SPDR Dow ETF
  We do this so we can pairs trade on our strategy relative to the Dow
  This both gives us a measure of how effective our strategy is relative to the market
  and reduces our risk.
  '''
  #Append most recent price so we can check later on if stock price increased after earnings
  for symbol in symbols[:-1]:
    (state.variables['history'][symbol]).append(prices[symbol])
  '''
  If we haven't initialized indices already, do so. 
  Do this by iterating through each stock's earnings calendar
  until the current date is within 7 days of the last earnings report.
  '''
  if not state.variables['init_indices']:
    for symbol in symbols[:-1]:
      while (state.time - state.earnings_dates[symbol][state.earnings_indices[symbol]].timestamp()) > 7 * 86400:
        state.earnings_indices[symbol]+=1
    state.variables['init_indices'] = True
  #Initialize buy list to 0 -- this will hold the stocks we open/keep positions in.  
  buy_list = []
  '''
  For each symbol except for the ETF, calculate the time between last earnings and now
  If it's 7 days (1 week) after earnings and price has increased, choose to open a position
  If it's after this, but before 2 weeks after earnings, choose to keep our current position open
  Otherwise, if we have an open position, it's ready to be closed, so we do so and increment the earnings index for that stock.
  '''
  for symbol in symbols[:-1]:
    diff = (state.time - state.earnings_dates[symbol][state.earnings_indices[symbol]].timestamp())
    if diff >= 7 * 86400 and diff <= 8 * 86400:
      if state.variables['history'][symbol][-1] > state.variables['history'][symbol][-6]:
        buy_list.append(symbol)
    elif state.variables['owns_position'][symbol] and diff >=8 * 86400 and diff <= 14 * 86400:
      buy_list.append(symbol)
    elif state.variables['owns_position'][symbol]:
      curr = blankly.trunc(state.interface.account[symbol].available, 2)
      if curr > 0:
        state.interface.market_order(symbol, side = 'sell', size = curr)
      state.variables['owns_position'][symbol] = False
      state.earnings_indices[symbol]+=1
  '''
  The buy list consists of tickers to hold positions (must be rebalanced)
  as well as tickers to open positions in. One way to rebalance is to sell all current holdings
  and then rebuy according to new allocations. This wouldn't be used in practice, as factors
  such as slippage make this worse than alternatives like simply selling and rebuying in a single transaction.
  However, for this slippage-free backtest, the two methods are equivalent, so we'll do this.
  '''    
  for symbol in buy_list:
    if state.variables['owns_position'][symbol]:
      #Get the amount of available shares of stock
      curr = blankly.trunc(state.interface.account[symbol].available, 2)
      state.interface.market_order(symbol, side = 'sell', size = curr)
      #sell and rebuy
  '''
  Here, we have the DIA logic for pairs trading. 
  If we own a DIA position, close it out.
  If we're going to buy stocks, open a new DIA position.
  Set the buy size for stocks to equal allocation of our cash across all stocks.
  '''
  if blankly.trunc(state.interface.account['DIA'].available, 2) < 0:
    state.interface.market_order('DIA', side ='buy', size = -blankly.trunc(state.interface.account['DIA'].available,2))
  if len(buy_list) > 0 :
    buy = state.interface.cash/len(buy_list)
    state.interface.market_order('DIA', side ='sell', size = blankly.trunc((state.interface.cash - prices['DIA'] * state.interface.account['DIA'].available)/(prices['DIA']),2))
  else:
    buy = 0
  #Loop through tickers in buy list and buy + set flag to True.
  for symbol in buy_list:
    if blankly.trunc(buy/prices[symbol], 2) > 0:
      state.interface.market_order(symbol, side ='buy', size = blankly.trunc(buy/(prices[symbol]), 2))
      state.variables['owns_position'][symbol] = True

if __name__ == "__main__":
    # Authenticate Alpaca Strategy
    exchange = blankly.Alpaca(portfolio_name="another cool portfolio")
    # Use our strategy helper on Alpaca
    strategy = blankly.Strategy(exchange)
    #Define our strategy on all 30 Dow stocks. 
    dow_stocks = ['AXP', 'AMGN', 'AAPL', 'BA', 'CAT', 'CSCO', 'CVX', 'GS', 'HD', 'HON', 'IBM', 'INTC','JNJ',\
                  'KO', 'JPM', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'CRM', 'VZ', 'V', 'WBA', 'WMT', 'DIS', 'DOW', 'DIA']
    # Run the event every time we check for a new price - once a day
    # The arbitrage event framework allows us to define strategies on groups of stocks together
    strategy.add_arbitrage_event(earn_event, dow_stocks, resolution='1d', init=init)
    # Start the strategy. This will begin each of the price event ticks
    strategy.start()
    # Or backtest using this
    #results = strategy.backtest(start_date='04/23/2021', end_date = '4/23/2022',initial_values={'USD': 10000})
    #print(results)
