import asyncio


class FrontRunningStrategy:
    def __init__(self, trade_executor, blockchain_interface):
        self.trade_executor = trade_executor
        self.blockchain_interface = blockchain_interface

    async def detect_opportunities(self):
        """Use WebSocket to monitor the mempool for large trades that haven't been confirmed yet."""
        async for tx in self.blockchain_interface.subscribe_unconfirmed_transactions():
            if self.is_large_trade(tx):
                trade_details = self.calculate_optimal_trade(tx)
                await self.trade_executor.execute_trade_async(trade_details)

    def is_large_trade(self, transaction):
        """Determine if the transaction involves a large volume."""
        return transaction['value'] > self.blockchain_interface.large_trade_threshold

    def calculate_optimal_trade(self, transaction):
        """Calculate the trade to place based on the detected transaction."""
        return {
            'type': 'buy',
            'asset': transaction['asset'],
            'amount': transaction['amount'],
            'price': transaction['price'] * 1.01
        }
