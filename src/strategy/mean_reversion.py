import numpy as np


class MeanReversion:
    def __init__(self, trade_executor, price_monitor):
        self.trade_executor = trade_executor
        self.price_monitor = price_monitor

    def find_opportunities(self):
        """Identify mean reversion opportunities based on asset price volatility."""
        assets = self.price_monitor.get_tradable_assets()
        for asset in assets:
            prices = self.price_monitor.get_historical_prices(asset)

            if len(prices) < 30:
                continue  # Ensure there is enough data

            prices = np.array(prices)
            average_price = np.mean(prices)
            current_price = prices[-1]
            volatility = np.std(prices[-30:])  # Calculate volatility based on the most recent 30 prices
            threshold = 2 * volatility  # Dynamic threshold based on recent volatility

            if current_price < average_price - threshold:
                self.trade_executor.execute_buy(asset, current_price)
            elif current_price > average_price + threshold:
                self.trade_executor.execute_sell(asset, current_price)
