from ib_insync import Stock

def gap_up_short_strategy(symbol, data):
    """Implement the Gap Up Short strategy."""
    print(f"Running Gap Up Short strategy for {symbol}...")

    # Ensure all required data is available
    opening_price = data.get("opening_price")
    last_price = data.get("last_price")
    previous_close = data.get("previous_close")  # Default to None if missing

    if opening_price is None or last_price is None or previous_close is None:
        print(f"Missing required data for {symbol}. Skipping Gap Up Short strategy.")
        return None

    # Gap-up logic: check if today's opening price is significantly higher than yesterday's close
    gap_up_threshold = 0.03  # Example: 3% gap up
    if opening_price > previous_close * (1 + gap_up_threshold):
        print(f"Gap Up Short signal triggered for {symbol}. Shorting at {last_price}.")
        contract = Stock(symbol, "SMART", "USD")
        return {
            "action": "SELL",
            "symbol": symbol,
            "quantity": 100,  # Fixed quantity
            "contract": contract,
            "price": last_price,  # Add price for clear execution
            "reason": "Gap Up Short",
        }

    print(f"No Gap Up Short signal for {symbol}.")
    return None
