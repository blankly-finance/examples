# Earnings Momentum Trading Bot - Alpaca

An Earnings Momentum trading bot that bets on stocks with positive earnings responses continuing to increase and beat the market. We test on the Dow 30.

## Getting Started

Note: Python Version 3.7+ is supported

1. First install Blankly using `pip`. Blankly is hosted on [PyPi](https://pypi.org/project/Blankly/). 
```bash
$ pip install blankly 
```
2. Clone the repo -- 
```
git clone https://github.com/blankly-finance/EarningsMomentum.git
```
3. Ensure that you have your Alpaca API Keys connected and set sandbox to true. Check [here](https://docs.blankly.finance/config/keys.json) for more details
4. Edit the python file and input your Financial Modeling Prep  API keys into the code (line 25)
5. Run the python file
```bash
$ python earningsbot.py 
```
6. Voila! You have a stock trading bot that trades off an Earnings Momentum Strategy.

## Backtest Output:
```
Calmar Ratio:                      1.96
Compound Annual Growth Rate (%):   11.0%
Conditional Value-at-Risk:         4.01
Cumulative Returns (%):            11.0%
Max Drawdown (%):                  4.0%
Resampled Time:                    86400.0
Risk Free Return Rate:             0.0
Sharpe Ratio:                      1.16
Sortino Ratio:                     1.47
Value-at-Risk:                     71.42
Variance (%):                      0.38%
Volatility:                        0.06
```
Also viewable [here](https://app.blankly.finance/RETIe0J8EPSQz7wizoJX0OAFb8y1/WyEGfaSW5F8nuEyVL62L/2462e91a-e21e-4cb7-af4b-c3f18df8e5e7/backtest).

## How does this work? 

This uses the [Blankly package](https://github.com/Blankly-Finance/Blankly) to build a [trading strategy](https://docs.blankly.finance/core/strategy)
We are able to utilize the `Blankly.Strategy` object to  create our arbitrage event that checks at every timestep whether a stock has a positive earnings response over a week timeframe. We can then use that, along with our earnings calendar, obtained through Financial Modeling Prep, to backtest our strategy on the past few years.

## What is the Earnings Momentum Strategy?

The Earnings Momentum Strategy is one of many momentum strategies, where instead of trying to predict the market's next moves, we ride the wave. Several momentum strategies have been shown to outperform the market over long time frames, and so building strategies around momentum is a great way to generate alpha. 
### Resources on Earnings Momentum
[Earnings Momentum - Investopedia](https://www.investopedia.com/terms/e/earnings_momentum.asp)
## Next Steps

Fork this repository and build on top of this strategy -- more stocks, different ways to hedge/pair trade, or whatever else you can think of. Take this strategy live by adding `strategy.start()` 

Join our [discord](https://discord.gg/xJAjGEAXNS) and check out our [platform](https://app.blankly.finance).
