# utils/config.py
import os
import json


def load_config():
    """Load configuration from a JSON file or environment variables."""
    config_path = os.getenv('BOT_CONFIG_PATH', 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    else:
        # Load configuration from environment variables if config file is not found
        return {
            'web3_provider': os.getenv('WEB3_PROVIDER'),
            'trader_address': os.getenv('TRADER_ADDRESS'),
            'private_key': os.getenv('PRIVATE_KEY'),
            'encryption_key': os.getenv('ENCRYPTION_KEY'),
            'api_key': os.getenv('API_KEY')
        }
