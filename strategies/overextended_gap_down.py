from ib_insync import Stock

def overextended_gap_down_strategy(symbol, data):
    """Implements the Overextended Gap Down strategy."""
    print(f"Running Overextended Gap Down strategy for {symbol}...")

    # Check for required data fields
    last_price = data.get("last_price")
    opening_price = data.get("opening_price")

    if last_price is None or opening_price is None:
        print(f"Error: Missing required data for {symbol}. Skipping Overextended Gap Down strategy.")
        return None

    # Strategy logic: Buy if the last price is significantly lower than the opening price
    if last_price < 0.90 * opening_price:  # Example threshold of a 10% gap down
        print(f"Overextended Gap Down signal triggered for {symbol}. Buying at {last_price}.")
        contract = Stock(symbol, "SMART", "USD")
        return {
            "symbol": symbol,
            "action": "BUY",
            "quantity": 100,  # Fixed quantity
            "contract": contract,
            "price": last_price,  # Added price for clarity in the trade signal
        }

    print(f"No Overextended Gap Down signal for {symbol}.")
    return None
