def gap_up_short_strategy(symbol, data):
    """Implement the Gap Up Short strategy."""
    print(f"Running Gap Up Short strategy for {symbol}...")

    # Ensure all required data is available
    if "opening_price" not in data or "last_price" not in data:
        print(f"Missing data for {symbol}. Skipping Gap Up Short strategy.")
        return None

    # Gap-up logic: check if today's opening price is significantly higher than yesterday's close
    opening_price = data["opening_price"]
    previous_close = data.get("previous_close")  # Default to None if missing

    if previous_close is None:
        print(f"Missing 'previous_close' for {symbol}. Cannot evaluate Gap Up Short strategy.")
        return None

    gap_up_threshold = 0.03  # Example: 3% gap up
    if opening_price > previous_close * (1 + gap_up_threshold):
        print(f"Gap Up Short signal triggered for {symbol}. Shorting at {data['last_price']}.")
        return {
            "action": "SELL",
            "symbol": symbol,
            "quantity": 100,
            "price": data["last_price"],
            "reason": "Gap Up Short"
        }
    else:
        print(f"No Gap Up Short signal for {symbol}.")
        return None
