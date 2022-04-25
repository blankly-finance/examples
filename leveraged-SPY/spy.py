# Risk On or Risk Off Leveraged S&P 500
from blankly import Alpaca, Strategy, StrategyState
from blankly.metrics import cum_returns
from blankly import trunc


def price_event(price, symbol, state: StrategyState):
    '''Buy and hold 'SPY' '''
    state.variables['history'].append(price)
    if state.variables['own_position'] == False:
        qty = int(state.interface.cash / price)
        state.interface.market_order(symbol, 'buy', qty)
        state.variables['own_position'] = True

def init(symbol, state: StrategyState):
    # Download price data of the 'SPY'
    state.variables['history'] =  state.interface.history(symbol, 150, resolution=state.resolution, return_as='deque')['close']
    state.variables['own_position'] = False


if __name__ == "__main__":
    # Authenticate Alpaca strategy
    exchange = Alpaca()

    # Use our strategy helper on Alpaca
    strategy = Strategy(exchange)

    # Run the compare price event function every time we check for a new price - by default that is 15 seconds
    strategy.add_price_event(price_event, 'SPY', resolution='1d', init=init)

    # Start the strategy. This will begin each of the price event ticks
    # strategy.start()
    # Or backtest using this
    results = strategy.backtest(to='2y', initial_values={'USD': 10000})
    print(results)
