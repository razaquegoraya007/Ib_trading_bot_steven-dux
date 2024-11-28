from ib_insync import Stock

def pre_market_breakout_strategy(symbol, data):
    """Implements the Pre-Market Breakout strategy."""
    print(f"Running Pre-Market Breakout strategy for {symbol}...")

    # Extract required data
    pre_market_high = data.get("pre_market_high")
    last_price = data.get("last_price")
    volume = data.get("volume")
    bid = data.get("bid")
    ask = data.get("ask")

    # Check for required fields
    if pre_market_high is None or last_price is None:
        print(f"Missing data for {symbol}. Skipping Pre-Market Breakout strategy.")
        return None

    # Validate price range
    if last_price < 5 or last_price > 20:
        print(f"{symbol} price {last_price} is out of the $5-$20 range. Skipping Pre-Market Breakout strategy.")
        return None

    # Strategy logic: Buy if the price breaks above the pre-market high
    if last_price > pre_market_high:
        print(f"Pre-Market Breakout signal triggered for {symbol}. Buying at {last_price}.")
        contract = data.get("contract") or Stock(symbol, "SMART", "USD")

        # Determine quantity dynamically based on the available volume (if applicable)
        quantity = 100  # Default to a fixed quantity if volume is not provided
        if volume and volume > 0:
            quantity = min(100, volume // 10)  # Example: Use 10% of the available volume, capped at 100

        return {
            "action": "BUY",
            "symbol": symbol,
            "quantity": quantity,
            "price": last_price,
            "contract": contract,
        }

    print(f"No Pre-Market Breakout signal for {symbol}.")
    return None
