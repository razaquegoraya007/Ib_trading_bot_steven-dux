def dip_buy_strategy(symbol, data):
    """Implements the Dip Buy strategy."""
    print(f"Running Dip Buy strategy for {symbol}...")
    last_price = data["last_price"]
    ask = data["ask"]

    # Example strategy logic: Buy if price is below a threshold
    if last_price < 0.95 * ask:
        print(f"Buy signal triggered for {symbol} at {last_price}.")
        return {
            "symbol": symbol,
            "action": "BUY",
            "price": last_price,
            "volume": 100,
        }
    else:
        print(f"No buy signal for {symbol}.")
        return None
