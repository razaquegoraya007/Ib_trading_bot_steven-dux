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

    # Strategy logic: Short if the price exceeds a threshold (5% above the bid price)
    bounce_threshold = 1.05  # Example threshold: 5% above the bid
    if last_price > bounce_threshold * bid:
        print(f"Bounce Short signal triggered for {symbol}. Shorting at {last_price}.")

        # Create the contract for the stock
        contract = Stock(symbol, "SMART", "USD")

        # Return trade signal with required fields
        return {
            "symbol": symbol,
            "action": "SELL",
            "quantity": 100,  # Define the quantity
            "contract": contract,
            "price": last_price,
            "reason": "Bounce Short",
        }

    print(f"No Bounce Short signal for {symbol}.")
    return None
