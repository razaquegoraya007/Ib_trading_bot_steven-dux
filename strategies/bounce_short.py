from ib_insync import Stock

def bounce_short_strategy(symbol, data):
    """Implements the Bounce Short strategy."""
    print(f"Running Bounce Short strategy for {symbol}...")

    # Safely access data fields
    last_price = data.get("last_price")
    bid = data.get("bid")

    # Ensure required data is present
    if last_price is None or bid is None:
        print(f"Missing required data for {symbol}. Skipping Bounce Short strategy.")
        return None

    # Strategy logic: Short if price exceeds a threshold
    if last_price > 1.05 * bid:
        print(f"Short signal triggered for {symbol} at {last_price}.")

        # Create the contract for the stock
        contract = Stock(symbol, "SMART", "USD")

        # Return trade signal with required fields
        return {
            "symbol": symbol,
            "action": "SELL",
            "quantity": 100,  # Define the quantity
            "contract": contract,
        }

    print(f"No short signal for {symbol}.")
    return None
