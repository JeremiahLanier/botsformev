import websocket
import json
import logging
from web3 import Web3
import backoff


class PriceMonitor:
    def __init__(self, web3: Web3, config: dict):
        self.web3 = web3
        self.config = config
        self.prices = {}  # Store prices keyed by token pair

    def on_message(self, ws, message):
        data = json.loads(message)
        # Assuming the API sends data in the format: {'pair': 'ETH/USD', 'price': 2500.0}
        pair = data['pair']
        price = data['price']
        self.prices[pair] = price
        logging.info(f"Received new price for {pair}: {price}")

    def on_error(self, ws, error):
        logging.error(f"WebSocket error: {error}")
        self.reconnect(ws)

    @backoff.on_exception(backoff.expo,
                          websocket.WebSocketException,
                          max_time=3600)  # Max backoff time 1 hour
    def reconnect(self, ws):
        logging.info("Reconnecting to WebSocket...")
        ws.run_forever()

    def on_close(self, ws, close_status_code, close_msg):
        logging.info("WebSocket connection closed")

    def on_open(self, ws):
        logging.info("WebSocket connection opened")
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": self.config['subscribed_pairs'],
            "id": 1
        }
        ws.send(json.dumps(subscribe_message))

    def start(self):
        websocket_url = self.config['websocket_url']
        ws = websocket.WebSocketApp(websocket_url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()


if __name__ == "__main__":
    from web3.auto import w3

    config = {
        'websocket_url': 'wss://api.exchange.com/ws',  # Placeholder for the actual WebSocket endpoint
        'subscribed_pairs': ['ETH/USD', 'BTC/USD']
    }
    price_monitor = PriceMonitor(w3, config)
    price_monitor.start()
