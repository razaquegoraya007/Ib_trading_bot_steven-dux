import os
import logging
from utils.data_loader import fetch_real_time_data
from utils.trade_executor import execute_trade
from strategies.bounce_short import bounce_short_strategy
from strategies.dip_buy import dip_buy_strategy
from strategies.first_red_day import first_red_day_strategy
from strategies.overextended_gap_down import overextended_gap_down_strategy
from strategies.pre_market_breakout import pre_market_breakout_strategy
from strategies.double_layer_resistance import double_layer_resistance_strategy
from strategies.gap_up_short import gap_up_short_strategy

# Set up logging
logging.basicConfig(filename="logs/trade_log.csv", level=logging.INFO, format="%(asctime)s,%(message)s")

def main():
    print("Starting trading bot...")
    symbols = ["AAPL", "AMZN", "MSFT"]
    strategies = [
        bounce_short_strategy,
        dip_buy_strategy,
        first_red_day_strategy,
        overextended_gap_down_strategy,
        pre_market_breakout_strategy,
        double_layer_resistance_strategy,
        gap_up_short_strategy,
    ]

    # Fetch real-time data for each symbol and apply strategies
    for symbol in symbols:
        print(f"\nFetching data for {symbol}...")
        data = fetch_real_time_data(symbol)
        if data is None:
            print(f"No data retrieved for {symbol}. Skipping...")
            continue

        for strategy in strategies:
            print(f"Executing {strategy.__name__} for {symbol}...")
            trade_signal = strategy(symbol, data)
            if trade_signal:
                execute_trade(trade_signal)

    print("Trading bot execution completed.")

if __name__ == "__main__":
    main()
