# utils/logger.py

import logging


def setup_logger():
    """Setup and configure the application logger."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger('TradingBotLogger')
