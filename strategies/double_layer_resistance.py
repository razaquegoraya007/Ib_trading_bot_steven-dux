from ib_insync import Stock

def double_layer_resistance_strategy(symbol, data):
    """Implements the Double Layer Resistance strategy."""
    print(f"Running Double Layer Resistance strategy for {symbol}...")

    # Get required data
    resistance_levels = data.get("resistance_levels")
    last_price = data.get("last_price")

    # Check for required fields
    if not resistance_levels or len(resistance_levels) < 2 or last_price is None:
        print(f"Missing required data for {symbol}. Skipping Double Layer Resistance strategy.")
        return None

    # Strategy logic: Short if price is between the two top resistance levels
    if resistance_levels[1] < last_price < resistance_levels[0]:
        print(f"Double Layer Resistance signal triggered for {symbol}. Selling at {last_price}.")
        contract = Stock(symbol, "SMART", "USD")
        return {
            "action": "SELL",
            "symbol": symbol,
            "quantity": 100,  # Example fixed quantity, adjustable as needed
            "contract": contract,
            "price": last_price,
            "reason": "Double Layer Resistance",
        }

    print(f"No Double Layer Resistance signal for {symbol}.")
    return None
