from ib_insync import Stock

def dip_buy_strategy(symbol, data):
    """Implements the Dip Buy strategy."""
    print(f"Running Dip Buy strategy for {symbol}...")

    # Get required data
    last_price = data.get("last_price")
    ask = data.get("ask")

    # Check for required fields
    if last_price is None or ask is None:
        print(f"Missing data for {symbol}. Skipping Dip Buy strategy.")
        return None

    # Strategy logic: Buy if the price is significantly below the ask price
    dip_threshold = 0.95  # Example threshold: 5% below the ask price
    if last_price < dip_threshold * ask:
        print(f"Dip Buy signal triggered for {symbol}. Buying at {last_price}.")
        contract = Stock(symbol, "SMART", "USD")
        return {
            "action": "BUY",
            "symbol": symbol,
            "quantity": 100,  # Example fixed quantity
            "contract": contract,
            "price": last_price,
            "reason": "Dip Buy",
        }

    print(f"No Dip Buy signal for {symbol}.")
    return None
