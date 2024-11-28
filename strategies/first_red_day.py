from ib_insync import Stock

def first_red_day_strategy(symbol, data):
    """Implements the First Red Day strategy."""
    print(f"Running First Red Day strategy for {symbol}...")

    # Get required data
    last_price = data.get("last_price")
    previous_close = data.get("previous_close")
    opening_price = data.get("opening_price")

    # Check for required fields
    if previous_close is None or last_price is None or opening_price is None:
        print(f"Missing required data for {symbol}. Skipping First Red Day strategy.")
        return None

    # Strategy logic: Short if price opens higher but drops below the previous close
    if opening_price > previous_close and last_price < previous_close:
        print(f"First Red Day signal triggered for {symbol}. Selling at {last_price}.")
        contract = Stock(symbol, "SMART", "USD")
        return {
            "action": "SELL",
            "symbol": symbol,
            "quantity": 50,  # Example quantity, adjustable based on account balance
            "contract": contract,
            "price": last_price,  # Add price for better execution clarity
            "reason": "First Red Day",
        }

    print(f"No First Red Day signal for {symbol}.")
    return None
