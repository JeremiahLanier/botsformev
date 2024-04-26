class SimpleArbitrage:
    def __init__(self, trade_executor, price_monitor):
        self.trade_executor = trade_executor
        self.price_monitor = price_monitor

    def find_opportunities(self):
        """Identify arbitrage opportunities and execute trades."""
        prices = self.price_monitor.get_prices()
        for pair in prices:
            if prices[pair]:  # Ensure there are prices to compare
                buy_exchange, buy_price = min(prices[pair].items(), key=lambda x: x[1])
                sell_exchange, sell_price = max(prices[pair].items(), key=lambda x: x[1])
                # Check if the arbitrage is profitable considering transaction costs
                if sell_price > buy_price * (1 + self.trade_executor.config['transaction_cost_percent']):
                    trade_details = {
                        'buy': {'exchange': buy_exchange, 'price': buy_price, 'pair': pair},
                        'sell': {'exchange': sell_exchange, 'price': sell_price, 'pair': pair}
                    }
                    if self.trade_executor.check_liquidity_and_execute(trade_details):
                        print(f"Executed arbitrage trade for {pair}, buying at {buy_exchange} and selling at {sell_exchange}")
