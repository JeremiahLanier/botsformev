import logging
from web3 import Web3

class TradeExecutor:
    def __init__(self, web3: Web3, config: dict):
        self.web3 = web3
        self.config = config
        self.active = True  # Controls trading activity based on conditions

    def calculate_optimal_gas_price(self):
        current_base_fee = self.web3.eth.fee_history(1, 'latest', [])[0]['baseFeePerGas']
        tip = self.config['max_priority_fee']
        if self.config['trade_urgency'] == 'high':
            tip *= 1.5
        elif self.config['trade_urgency'] == 'low':
            tip *= 0.5
        return current_base_fee + tip

    def is_profitable(self, trade, current_prices):
        buy_price = current_prices[trade['buy']['market']][trade['buy']['pair']]
        sell_price = current_prices[trade['sell']['market']][trade['sell']['pair']]
        return sell_price > buy_price * (1 + self.config['minimum_profit_threshold'])

    def execute_trade(self, trade):
        if not self.active:
            logging.info("Trading is currently paused.")
            return
        gas_price = self.calculate_optimal_gas_price()
        contract = self.web3.eth.contract(address=trade['contract_address'], abi=trade['abi'])
        tx = contract.functions.trade(trade['amount']).buildTransaction({
            'from': self.config['trader_address'],
            'gas': self.config['gas_limit'],
            'gasPrice': gas_price,
            'nonce': self.web3.eth.getTransactionCount(self.config['trader_address'])
        })
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.config['private_key'])
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        logging.info(f"Executed trade with tx hash: {tx_hash.hex()}")
        return tx_hash

    def execute_multi_leg_trade(self, trade_legs):
        for leg in trade_legs:
            self.execute_trade(leg)

    def emergency_stop(self):
        self.active = False
        logging.info("Emergency stop activated.")

    def log_trade(self, trade, tx_hash, status):
        logging.info(f"Trade {trade['id']} executed. Tx: {tx_hash.hex()}, Status: {status}")

    def check_slippage(self, trade, current_prices):
        expected_price = current_prices[trade['buy']['market']][trade['buy']['pair']]
        max_slippage = expected_price * self.config['max_slippage_percentage']
        return trade['execute_price'] <= expected_price + max_slippage

    def decide_trades(self, potential_trades, current_prices):
        trades_to_execute = []
        for trade in potential_trades:
            if self.is_profitable(trade, current_prices) and self.check_slippage(trade, current_prices):
                trades_to_execute.append(trade)
        return trades_to_execute

if __name__ == "__main__":
    from web3.auto import w3
    config = {
        'trader_address': '0xYourTraderAddress',
        'private_key': 'your-private-key',
        'gas_limit': 200000,
        'gas_price': 10,  # In gwei
        'max_priority_fee': 2,  # In gwei
        'trade_urgency': 'normal',
        'minimum_profit_threshold': 0.01,  # 1%
        'max_slippage_percentage': 0.02  # 2%
    }
    trade_executor = TradeExecutor(w3, config)
    # Example usage
    potential_trades = [{'buy': {'market': 'Uniswap', 'pair': 'ETH/USD'}, 'sell': {'market': 'Sushiswap', 'pair': 'ETH/USD'}}]
    current_prices = {'Uniswap': {'ETH/USD': 2500}, 'Sushiswap': {'ETH/USD': 2510}}
    trades_to_execute = trade_executor.decide_trades(potential_trades, current_prices)
    for trade in trades_to_execute:
        trade_executor.execute_trade(trade)
