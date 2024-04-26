import logging
import logging
from web3 import Web3
from trade_executor import TradeExecutor
from lib.blockchain_interface import BlockchainInterface
from strategy.front_running import FrontRunningStrategy
from strategy.back_running import BackRunningStrategy
from strategy.sandwich_trades import SandwichTradingStrategy
from utils.config import load_config
from utils.logger import setup_logger
from utils.security import SecurityManager
from utils.performance_monitoring import PerformanceMonitor
from utils.feature_toggles import FeatureToggle


def main():
    # Setup logging
    logger = setup_logger()

    # Load configuration
    config = load_config()
    web3 = Web3(Web3.HTTPProvider(config['web3_provider']))
    if not web3.isConnected():
        logger.error("Failed to connect to the Ethereum network")
        return

    # Initialize the Security Manager with the encryption key from the config
    security_manager = SecurityManager(config['encryption_key'])

    # Initialize the Trade Executor
    trade_executor = TradeExecutor(web3, config)

    # Initialize the Blockchain Interface
    blockchain_interface = BlockchainInterface(web3)

    # Initialize trading strategies
    front_running = FrontRunningStrategy(trade_executor, blockchain_interface)
    back_running = BackRunningStrategy(trade_executor, blockchain_interface)
    sandwich_trading = SandwichTradingStrategy(trade_executor, blockchain_interface)

    # Feature toggles to enable/disable specific strategies
    feature_toggle = FeatureToggle()
    feature_toggle.set_feature('enable_front_running', True)
    feature_toggle.set_feature('enable_back_running', True)
    feature_toggle.set_feature('enable_sandwich_trades', True)

    # Start strategy operations based on feature toggles
    if feature_toggle.is_enabled('enable_front_running'):
        logger.info("Front running strategy enabled.")
        front_running.detect_opportunities()
    if feature_toggle.is_enabled('enable_back_running'):
        logger.info("Back running strategy enabled.")
        back_running.monitor_transactions()
    if feature_toggle.is_enabled('enable_sandwich_trades'):
        logger.info("Sandwich trading strategy enabled.")
        sandwich_trading.detect_target_transactions()

    # Setup Performance Monitoring
    performance_monitor = PerformanceMonitor()
    performance_monitor.log_performance()

    logger.info("Trading bot setup complete and operational.")


if __name__ == "__main__":
    main()
