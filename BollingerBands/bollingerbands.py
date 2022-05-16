import blankly

def init(symbol, state: blankly.StrategyState):
    # Download price data for initialization
    state.variables['history'] = state.interface.history(symbol, to=50, return_as='list',
                                                         resolution=state.resolution)['close']
    state.variables['owns_position'] = False

def price_event(price, symbol, state: blankly.StrategyState):
    """ This function will give an updated price every 15 seconds from our definition below """
    state.variables['history'].append(price)
    # exit if we don't have enough populated information yet
    if len(state.variables['history']) < 14:
        return
    #Calculate bollinger bands for the current time based off the last 14 time periods
    bbands = blankly.indicators.bbands(state.variables['history'][-14:])
    #Lower bollinger band
    bbands_low = bbands[0]
    #Higher bollinger band
    bbands_high = bbands[2]

    #If price crosses under bollinger band, we buy
    if bbands_low > price and not state.variables['owns_position']:
      if blankly.trunc(state.interface.cash/price,2) > 0:
        state.interface.market_order(symbol, side='buy', size= blankly.trunc(state.interface.cash/price,2))
        state.variables['owns_position'] = True
    #Sell when price crosses back between bands
    elif (bbands_low < price and state.variables['owns_position']):
      sell = blankly.trunc(state.interface.account[state.base_asset].available, 2)
      if sell > 0:
        state.interface.market_order(symbol, side = 'sell', size = sell)
        state.variables['owns_position'] = False

if __name__ == "__main__":
    # Authenticate FTX Strategy
    exchange = blankly.FTX()
    # Use our strategy helper on FTX
    strategy = blankly.Strategy(exchange)

    # Run the price event function every time we check for a new price
    strategy.add_price_event(price_event, symbol='SOL-USD', resolution='1d', init=init)
    # Start the strategy. This will begin each of the price event ticks
    # strategy.start()
    # Or backtest using this
    results = strategy.backtest(to='1y', initial_values={'USD': 10000})
    print(results)