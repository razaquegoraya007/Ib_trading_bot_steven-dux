from ib_insync import Stock

def pre_market_breakout_strategy(symbol, data):
    """Implements the Pre-Market Breakout strategy."""
    print(f"Running Pre-Market Breakout strategy for {symbol}...")

    # Get required data
    pre_market_high = data.get("pre_market_high")
    last_price = data.get("last_price")

    # Check for required fields
    if pre_market_high is None or last_price is None:
        print(f"Missing data for {symbol}. Skipping Pre-Market Breakout strategy.")
        return None

    # Strategy logic: Buy if the price breaks above the pre-market high
    if last_price > pre_market_high:
        print(f"Pre-Market Breakout signal triggered for {symbol}. Buying at {last_price}.")
        contract = Stock(symbol, "SMART", "USD")
        return {
            "action": "BUY",
            "symbol": symbol,
            "quantity": 100,  # Example fixed quantity
            "contract": contract,
        }

    print(f"No Pre-Market Breakout signal for {symbol}.")
    return None
