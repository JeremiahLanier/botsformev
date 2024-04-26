class TriangularArbitrage:
    def __init__(self, trade_executor, price_monitor):
        self.trade_executor = trade_executor
        self.price_monitor = price_monitor

    def find_opportunities(self, exchange):
        """Scan for triangular arbitrage opportunities on a single exchange."""
        currency_pairs = self.price_monitor.get_currency_pairs(exchange)
        for base in currency_pairs:
            for quote in currency_pairs[base]:
                for intermediate in currency_pairs[quote]:
                    if base in currency_pairs[intermediate]:
                        # Calculate potential profitability
                        start_amount = 1  # Starting with 1 unit
                        step1 = start_amount * currency_pairs[base][quote]
                        step2 = step1 * currency_pairs[quote][intermediate]
                        final_amount = step2 * currency_pairs[intermediate][base]
                        if final_amount > start_amount * (1 + self.trade_executor.config['minimum_profit_threshold']):
                            trade_details = {
                                'steps': [
                                    {'action': 'buy', 'pair': (base, quote), 'amount': start_amount},
                                    {'action': 'buy', 'pair': (quote, intermediate), 'amount': step1},
                                    {'action': 'sell', 'pair': (intermediate, base), 'amount': step2}
                                ],
                                'final_amount': final_amount
                            }
                            self.trade_executor.execute_triangular_trade(trade_details)
