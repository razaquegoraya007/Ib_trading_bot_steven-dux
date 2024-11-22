def overextended_gap_down_strategy(symbol, data):
    """Implements the Overextended Gap Down strategy."""
    print(f"Running Overextended Gap Down strategy for {symbol}...")

    if "opening_price" not in data:
        print(f"Error: 'opening_price' data is missing for {symbol}. Skipping strategy.")
        return None

    last_price = data["last_price"]
    opening_price = data["opening_price"]

    # Example logic: Buy if there is a significant gap down in the opening price
    if last_price < 0.90 * opening_price:
        print(f"Overextended Gap Down signal triggered for {symbol}. Buying at {last_price}.")
        return {
            "symbol": symbol,
            "action": "BUY",
            "price": last_price,
            "volume": 100,
        }
    else:
        print(f"No Overextended Gap Down signal for {symbol}.")
        return None
