import numpy as np
from statsmodels.api import OLS
import pandas as pd


class PairsTrading:
    def __init__(self, trade_executor, price_monitor):
        self.trade_executor = trade_executor
        self.price_monitor = price_monitor

    def find_opportunities(self):
        """Identify pairs trading opportunities based on historical price relationships."""
        pairs = self.price_monitor.get_tradable_pairs()
        for asset1, asset2 in pairs:
            prices1 = self.price_monitor.get_historical_prices(asset1)
            prices2 = self.price_monitor.get_historical_prices(asset2)

            if len(prices1) == 0 or len(prices2) == 0:
                continue  # Skip if no price data available

            # Calculate the hedge ratio using linear regression
            hedge_ratio = self.calculate_hedge_ratio(prices1, prices2)

            # Calculate the spread
            spread = np.array(prices1) - hedge_ratio * np.array(prices2)
            mean_spread = np.mean(spread)
            std_dev_spread = np.std(spread)

            # Look for the spread deviation
            current_spread = spread[-1]
            if abs(current_spread - mean_spread) > 2 * std_dev_spread:
                amount = abs(current_spread - mean_spread) / std_dev_spread
                self.trade_executor.execute_pairs_trade(asset1, asset2, amount, current_spread > mean_spread)

    def calculate_hedge_ratio(self, prices1, prices2):
        """Calculate the hedge ratio using linear regression."""
        model = OLS(prices1, prices2).fit()
        return model.params[0]
