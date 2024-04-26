# utils/data_utils.py

import json
import pandas as pd


def load_historical_prices(filepath):
    return pd.read_csv(filepath)


def save_trading_log(log, filepath):
    with open(filepath, 'a') as file:
        json.dump(log, file)
        file.write('\n')  # Newline for each log entry


def load_trading_log(filepath):
    with open(filepath, 'r') as file:
        return [json.loads(line) for line in file]
