import websocket
import json
import logging
from web3 import Web3
import backoff

class MempoolMonitor:
    def __init__(self, web3: Web3, config: dict):
        self.web3 = web3
        self.config = config

    def start_realtime_monitor(self):
        """Start monitoring the mempool in real-time using WebSocket."""
        websocket_url = self.config.get('websocket_url')
        ws = websocket.WebSocketApp(websocket_url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

    def on_message(self, ws, message):
        data = json.loads(message)
        tx = data.get('transaction')
        if tx and self.is_interesting_tx(tx):
            logging.info(f"Interesting transaction detected: {tx}")

    def on_error(self, ws, error):
        logging.error(f"WebSocket error: {error}")
        self.reconnect(ws)

    @backoff.on_exception(backoff.expo,
                          websocket.WebSocketException,
                          max_time=300)
    def reconnect(self, ws):
        logging.info("Attempting to reconnect...")
        ws.run_forever()

    def on_close(self, ws, close_status_code, close_msg):
        logging.info("WebSocket connection closed")

    def on_open(self, ws):
        logging.info("WebSocket connection opened")
        ws.send(json.dumps({"method": "subscribe", "params": ["newPendingTransactions"]}))

    def is_interesting_tx(self, tx):
        """Determine if a transaction is 'interesting' based on predefined criteria."""
        # Example: Filter for high gas prices or to specific contracts
        return tx['to'] in self.config['watched_addresses'] and tx['gasPrice'] >= self.config['min_gas_price']

if __name__ == "__main__":
    from web3.auto import w3
    config = {
        'websocket_url': 'wss://your_eth_node.com/ws',
        'watched_addresses': ['0x...', '0x...'],
        'min_gas_price': 100 * 10**9  # 100 Gwei
    }
    mempool_monitor = MempoolMonitor(w3, config)
    mempool_monitor.start_realtime_monitor()
