import logging
from utils.data_loader import fetch_all_stocks, fetch_real_time_data
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

PRICE_RANGE = (5, 20)

# Track trades
trades = []

def log_trade_result(symbol, action, quantity, entry_price, exit_price=None):
    profit = None
    percentage = None

    if exit_price is not None:
        profit = (exit_price - entry_price) * quantity if action == "BUY" else (entry_price - exit_price) * quantity
        percentage = ((exit_price - entry_price) / entry_price) * 100 if action == "BUY" else ((entry_price - exit_price) / entry_price) * 100

    trades.append({
        "symbol": symbol,
        "action": action,
        "quantity": quantity,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "profit": profit,
        "percentage": percentage
    })

    logging.info(f"{symbol},{action},{quantity},{entry_price},{exit_price},{profit},{percentage}")

def display_summary():
    total_profit = sum(trade["profit"] for trade in trades if trade["profit"] is not None)
    total_trades = len(trades)
    winning_trades = sum(1 for trade in trades if trade["profit"] and trade["profit"] > 0)
    losing_trades = total_trades - winning_trades

    print("\nPerformance Summary:")
    print(f"Total Trades Executed: {total_trades}")
    print(f"Winning Trades: {winning_trades}")
    print(f"Losing Trades: {losing_trades}")
    print(f"Total Profit/Loss: ${total_profit:.2f}")
    print(f"Win Rate: {winning_trades / total_trades * 100:.2f}%")

def main():
    print("Starting trading bot...")
    print("Scanning for stocks within the $5-$20 price range...")

    all_stocks = fetch_all_stocks()
    print(f"Total stocks found: {len(all_stocks)}")

    filtered_symbols = []
    for symbol in all_stocks:
        data = fetch_real_time_data(symbol)

        # Validate the data and filter by price range
        if data and PRICE_RANGE[0] <= data["last_price"] <= PRICE_RANGE[1]:
            filtered_symbols.append(symbol)
        else:
            print(f"Skipping {symbol}: Not within range or invalid data.")

    print(f"Filtered stocks within range: {filtered_symbols}")

    strategies = [
        bounce_short_strategy,
        dip_buy_strategy,
        first_red_day_strategy,
        overextended_gap_down_strategy,
        pre_market_breakout_strategy,
        double_layer_resistance_strategy,
        gap_up_short_strategy,
    ]

    for symbol in filtered_symbols:
        print(f"\nFetching data for {symbol}...")
        data = fetch_real_time_data(symbol)

        if data is None:
            print(f"No data retrieved for {symbol}. Skipping...")
            continue

        for strategy in strategies:
            print(f"Executing {strategy.__name__} for {symbol}...")
            trade_signal = strategy(symbol, data)
            if trade_signal:
                result = execute_trade(trade_signal)
                if result:
                    log_trade_result(
                        symbol=result["symbol"],
                        action=result["action"],
                        quantity=result["quantity"],
                        entry_price=result["entry_price"],
                        exit_price=result.get("exit_price")
                    )

    display_summary()
    print("Trading bot execution completed.")

if __name__ == "__main__":
    main()
