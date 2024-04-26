class BackRunningStrategy:
    def __init__(self, trade_executor, blockchain_interface):
        self.trade_executor = trade_executor
        self.blockchain_interface = blockchain_interface

    def monitor_transactions(self):
        """Attach to blockchain event listener for high-impact transactions."""
        self.blockchain_interface.on_new_confirmed_transactions(self.handle_transaction)

    def handle_transaction(self, tx):
        """Respond to newly confirmed transactions with potential market impact."""
        if self.affects_market(tx):
            trade_details = self.create_follow_up_trade(tx)
            self.trade_executor.execute_trade(trade_details)

    def affects_market(self, transaction):
        """Check if the transaction is likely to have a significant market impact."""
        return transaction['value'] > self.blockchain_interface.market_impact_threshold
