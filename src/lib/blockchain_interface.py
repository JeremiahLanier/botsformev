from web3 import Web3


class BlockchainInterface:
    def __init__(self, web3_url):
        """Initialize the Web3 connection."""
        self.web3 = Web3(Web3.HTTPProvider(web3_url))
        if not self.web3.isConnected():
            raise ValueError("Failed to connect to the Ethereum network")

    def get_unconfirmed_transactions(self):
        """Retrieve unconfirmed transactions from the Ethereum mempool."""
        return self.web3.eth.get_block('pending', full_transactions=True).transactions

    def get_recently_confirmed_transactions(self):
        """Retrieve the latest block and return its transactions, assuming it's confirmed."""
        latest_block = self.web3.eth.get_block('latest', full_transactions=True)
        return latest_block.transactions

    def subscribe_to_transactions(self, callback):
        """Subscribe to new transactions using a filter."""
        transaction_filter = self.web3.eth.filter('pending')
        transaction_filter.watch(callback)

    def subscribe_to_new_blocks(self, callback):
        """Subscribe to new blocks as they are discovered."""
        block_filter = self.web3.eth.filter('latest')
        block_filter.watch(callback)
