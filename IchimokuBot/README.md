# Ichimoku Cloud Trading Bot - Alpaca

A Ichimoku Cloud-based trading bot that allocates position sizes based on the Ichimoku Cloud to trade stocks (GME).

## Getting Started

Note: Python Version 3.7+ is supported

1. First install Blankly using `pip`. Blankly is hosted on [PyPi](https://pypi.org/project/Blankly/). 
```bash
$ pip install blankly 
```
2. Clone the repo -- 
```
git clone https://github.com/blankly-finance/IchimokuBot.git
```
3. Ensure that you have your Alpaca API Keys connected and set sandbox to true. Check [here](https://docs.blankly.finance/config/keys.json) for more details
4. Run the python file
```bash
$ python ichimokucloud.py 
```
5. Voila! You have a stock trading bot that works based off the Kelly Criterion!

## Backtest Output:
```
Blankly Metrics: 
Calmar Ratio: 2.63
Compound Annual Growth Rate (%): 233.0% 
Conditional Value-at-Risk: 69.1
Cumulative Returns (%): 3559.0% 
Max Drawdown (%): 79.0% 
Resampled Time: 86400.0
Risk-Free Return Rate: 0.0
Sharpe Ratio: 0.95
Sortino Ratio: 2.59
Volatility: 2.18 
Value-at-Risk: 1044.72 
Variance (%): 474.64%
```
Also viewable [here](https://app.blankly.finance/RETIe0J8EPSQz7wizoJX0OAFb8y1/wzmUrgnjaBwcsSrwSPKx/e41328c8-6c32-409c-9c0c-77456c7826e6/backtest).

## How does this work? 

This uses the [Blankly package](https://github.com/Blankly-Finance/Blankly) to build a [trading strategy](https://docs.blankly.finance/core/strategy)
We are able to utilize the `Blankly.Strategy` object to easily create our price event that computes the Ichimoku Cloud, sets stop losses and profit targets, and generates a buy or sell signal based on the price action relative to the cloud. Once we add a ticker to the price event, we can backtest or live trade our strategy.

## What is the Ichimoku Cloud?

The [Ichimoku Cloud](https://www.investopedia.com/terms/i/ichimoku-cloud.asp) is a technical indicator system that works off of the past low and high prices across a set of time periods. It was released in the 1960s by Goichi Hosoda and given a resolution generates a "cloud" -- a region between two lines along with an orientation (green or red). Price action breaking out of this "cloud" can be used as a signal to buy or sell.
### Resources on Ichimoku Cloud
[Ichimoku Cloud - StockCharts](https://school.stockcharts.com/doku.php?id=technical_indicators:ichimoku_cloud)
## Next Steps

Fork this repository, and start adding in some more [indicators](https://docs.blankly.finance/metrics/indicators) to also. Take this strategy live by adding `strategy.start()` 

Join our [discord](https://discord.gg/xJAjGEAXNS) and check out our [platform](https://app.blankly.finance).
