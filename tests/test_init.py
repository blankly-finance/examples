import importlib
import json
import os
import time
import unittest
import shutil
import runpy
import blankly

current_quote_setting = 'USD'


def change_quote_setting(symbol: str):
    global current_quote_setting
    if symbol != current_quote_setting:
        # Read and change
        file = open('./backtest.json', 'r')
        contents = json.loads(file.read())
        contents['settings']['quote_account_value_in'] = symbol
        file.close()

        # Write it in
        file = open('./backtest.json', 'w')
        file.write(json.dumps(contents, indent=2))
        file.close()

        current_quote_setting = symbol


# TODO remove this when the better key sandbox management comes out
def change_live_setting(live: bool):
    # Read and change
    file = open('./settings.json', 'r')
    contents = json.loads(file.read())
    contents['settings']['use_sandbox'] = live
    file.close()

    # Write it in
    file = open('./settings.json', 'w')
    file.write(json.dumps(contents, indent=2))
    file.close()


class TestInit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.exchanges = ['binance', 'alpaca', 'ftx', 'alpaca', 'oanda', 'coinbase_pro', 'ftx']
        cls.test_files = os.listdir('./init')

        # Put a settings in the root for all scripts
        shutil.copyfile('./configs/settings.json', './settings.json')
        shutil.copyfile('./configs/backtest_usd.json', './backtest.json')

    def test_init(self):
        for i in self.exchanges:
            if i == 'binance':
                change_live_setting(False)
            else:
                change_live_setting(True)

            # Swap the quote and run them
            if i == 'binance' or i == 'kucoin':
                change_quote_setting('USDT')
            else:
                change_quote_setting('USD')

            runpy.run_path(f'./init/rsi_{i}.py', {}, "__main__")

            # Reload the utils module so that the old settings cache doesn't stick around
            blankly.utils = importlib.reload(blankly.utils)
