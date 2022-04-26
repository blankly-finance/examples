import numpy as np
import blankly

def init(symbol, state: blankly.StrategyState):
    # Download price data for initialization
    state.variables['history'] = state.interface.history(symbol, to=300, return_as='list',
                                                         resolution=state.resolution)['close']
    state.variables['owns_position'] = False
    state.variables['take_profit'] = 0
    state.variables['stop_loss'] = 0

    state.variables['leading_span_a'] = np.zeros(len(state.variables['history']), dtype=np.float64)
    state.variables['leading_span_b'] = np.zeros(len(state.variables['history']), dtype=np.float64)
    # Compute span data for the initial data points
    for i in range(26, len(state.variables['history'])):
      state.variables['leading_span_a'][i] = ((np.max(state.variables['history'][i-26:i]) + np.min(state.variables['history'][i-26:i]))/2 + \
                                              (np.max(state.variables['history'][i-9:i]) + np.min(state.variables['history'][i-9:i]))/2)/2
    for i in range(52, len(state.variables['history'])):
      state.variables['leading_span_b'][i] = (np.max(state.variables['history'][i-52:i]) + np.min(state.variables['history'][i-52:i]))/2

def price_event(price, symbol, state: blankly.StrategyState):
    """ This function will give an updated price every 15 seconds from our definition below """
    state.variables['history'].append(price)
    # exit if we don't have enough populated information yet
    if len(state.variables['history']) < 78:
        return 

    conversion = (np.max(state.variables['history'][-9:]) + np.min(state.variables['history'][-9:]))/2
    base = (np.max(state.variables['history'][-26:]) + np.min(state.variables['history'][-26:]))/2
    leading_span_a = (conversion + base)/2
    leading_span_b = (np.max(state.variables['history'][-52:]) + np.min(state.variables['history'][-52:]))/2

    state.variables['leading_span_a'] = np.append(state.variables['leading_span_a'], leading_span_a)
    state.variables['leading_span_b'] = np.append(state.variables['leading_span_b'], leading_span_b)   
    
    # If we already own a position, look for take profit or stop loss
    if state.variables['owns_position']:
        if (price <= state.variables['stop_loss'] or price >= state.variables['take_profit']):
            # Dollar cost average sell
            curr_value = blankly.trunc(state.interface.account[state.base_asset].available, 2)
            state.interface.market_order(symbol, side='sell', size=curr_value)
            print("\nExiting Long Position ...")
            state.variables['owns_position'] = False
        return
        
    top_of_cloud_past = max(state.variables['leading_span_a'][-52], state.variables['leading_span_b'][-52])
    bottom_of_cloud_past = min(state.variables['leading_span_a'][-52], state.variables['leading_span_b'][-52])
    top_of_cloud_current = max(state.variables['leading_span_a'][-26], state.variables['leading_span_b'][-26])
    bottom_of_cloud_current = min(state.variables['leading_span_a'][-26], state.variables['leading_span_b'][-26])
    cloud_green_in_future = leading_span_a - leading_span_b # green if positive
    # BUY SIGNAL
    if (price > top_of_cloud_current) and (conversion > base) and \
        (cloud_green_in_future > 0) and (price > top_of_cloud_past):
        if not state.variables['owns_position']:
            # Buy with full capital
            buy = blankly.trunc(state.interface.cash/price, 2)
            state.interface.market_order(symbol, side='buy', size=buy)
            print("\nEntered Long Position ...")
            state.variables['owns_position'] = True
            state.variables['stop_loss'] = bottom_of_cloud_current
            state.variables['take_profit'] = price + (price - bottom_of_cloud_current) * 1.7

def price_baseline(price,symbol,state: blankly.StrategyState):
	buy = blankly.trunc(state.interface.cash/price, 2)
	if buy > 0:
		state.interface.market_order(symbol, side='buy', size=buy)

if __name__ == "__main__":
    # Authenticate Alpaca Strategy
    exchange = blankly.Alpaca(portfolio_name="another cool portfolio")
    # Use our strategy helper on Alpaca
    strategy = blankly.Strategy(exchange)

    # Run the price event function every time we check for a new price - by default that is 15 seconds
    strategy.add_price_event(price_event, symbol='GME', resolution='1h', init=init)
    # Start the strategy. This will begin each of the price event ticks
    # strategy.start()
    # Or backtest using this
    results = strategy.backtest(to='3y', initial_values={'USD': 10000})
    print(results)