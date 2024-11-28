import time

WATCHLIST = {}
WATCHLIST_EXPIRY_DAYS = 7

def manage_watchlist():
    """Manages the stock watchlist and returns the active symbols."""
    global WATCHLIST
    current_time = time.time()

    # Remove expired stocks
    WATCHLIST = {symbol: added_time for symbol, added_time in WATCHLIST.items()
                 if current_time - added_time < WATCHLIST_EXPIRY_DAYS * 86400}

    # Add new stocks to the watchlist (example logic, can be replaced with actual criteria)
    new_stocks = ["AAPL", "AMZN", "MSFT"]
    for stock in new_stocks:
        if stock not in WATCHLIST:
            WATCHLIST[stock] = current_time

    return list(WATCHLIST.keys())
