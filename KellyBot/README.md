# Kelly Criterion Trading Bot - Alpaca

A RSI-based trading bot that allocates position sizes based on the Kelly Criterion to trade stocks (SPY, CRM, AAPL).

## Getting Started

Note: Python Version 3.7+ is supported

1. First install Blankly using `pip`. Blankly is hosted on [PyPi](https://pypi.org/project/Blankly/). 
```bash
$ pip install blankly 
```
2. Clone the repo -- 
```
git clone https://github.com/blankly-finance/KellyBot.git
```
3. Ensure that you have your Alpaca API Keys connected and set sandbox to true. Check [here](https://docs.blankly.finance/config/keys.json) for more details
4. Run the python file
```bash
$ python kellybot.py 
```
5. Voila! You have a stock trading bot that works based off the Kelly Criterion!

## Backtest Output:
```
Blankly Metrics: 
Calmar Ratio: 3.42
Compound Annual Growth Rate (%): 22.0% 
Conditional Value-at-Risk: 1.02
Cumulative Returns (%): 22.0% 
Max Drawdown (%): 4.0% 
Resampled Time: 86400.0
Risk-Free Return Rate: 0.0
Sharpe Ratio: 1.95
Sortino Ratio: 3.58
Volatility: 0.07 
Value-at-Risk: 58.84 
Variance (%): 0.52%
```

## How does this work? 

This uses the [blankly package](https://github.com/Blankly-Finance/Blankly) to build a [trading strategy](https://docs.blankly.finance/core/strategy)
We are able to utilize the `Blankly.Strategy` object to easily add our Kelly initialization function that determines our RSI histogram logic and calculations and then easily create a price event that trades off of the calculated Kelly Criterion sizes.

## What is Kelly Criterion?

The [Kelly Criterion](https://blankly.finance/the-kelly-criterion) gives the optimal bet value, given the probabilities of wins and losses as well as the payoffs for each outcome. It works by optimizing the logarithmic growth rate, which leads to the greatest returns in the long term. In portfolio management scenarios, where it's important to both discover opportunities and allocate capital efficiently, the Kelly Criterion is an extremely useful tool. 

### Resources on Kelly Criterion

[What is Kelly? - Investopedia](https://www.investopedia.com/articles/trading/04/091504.asp)
[The Kelly Criterion](https://blogs.cfainstitute.org/investor/2018/06/14/the-kelly-criterion-you-dont-know-the-half-of-it/)

## Next Steps

Fork this repository, and start adding in some more [indicators](https://docs.blankly.finance/metrics/indicators) to test different ways to build the base model. Alternatively, build the Kelly Criterion section onto one of your existing models.
Take this strategy live by changing it to `strategy.start()` or use `strategy.backtest()` to backtest.

Join our [discord](https://discord.gg/xJAjGEAXNS) and check out our [platform](https://app.blankly.finance).
