import logging
from ib_insync import MarketOrder, IB

# Initialize trade log
TRADE_LOG = {}

def execute_trade(signal):
    """Execute trade based on the signal."""
    ib = IB()
    try:
        print("Connecting to IB Gateway for trade execution...")
        ib.connect("127.0.0.1", 4001, clientId=2)

        # Extract details from signal
        action = signal.get("action")
        symbol = signal.get("symbol")
        quantity = signal.get("quantity", 100)
        contract = signal.get("contract")
        price = signal.get("price")

        if not action or not symbol or not contract or not price:
            print("Invalid signal. Missing action, symbol, price, or contract.")
            return None

        print(f"Placing order: {action} {quantity} {symbol} at market price.")
        order = MarketOrder(action, quantity)
        trade = ib.placeOrder(contract, order)

        # Log trade details and calculate potential P&L
        result = log_trade(symbol, action, quantity, price)
        print(f"Order placed: {trade}")

        return result

    except Exception as e:
        print(f"Error executing trade: {e}")
        return None
    finally:
        print("Disconnecting from IB Gateway after trade execution...")
        ib.disconnect()

def log_trade(symbol, action, quantity, entry_price, exit_price=None):
    """Log trade details."""
    global TRADE_LOG
    trade_data = {
        "symbol": symbol,
        "action": action,
        "quantity": quantity,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "profit": None,
    }

    # Calculate profit/loss if it's a closing trade
    if exit_price is not None:
        previous_trade = TRADE_LOG.get(symbol)
        if previous_trade and previous_trade["action"] != action:
            profit = (exit_price - previous_trade["entry_price"]) * quantity
            profit = profit if previous_trade["action"] == "BUY" else -profit
            trade_data["profit"] = profit

            print(f"Profit/Loss for {symbol}: {profit:.2f}")
            logging.info(f"Profit/Loss for {symbol}: {profit:.2f}")

            # Remove the trade from the log after calculating P&L
            del TRADE_LOG[symbol]
        else:
            print(f"No matching trade to calculate P&L for {symbol}.")

    # Log trade data
    TRADE_LOG[symbol] = trade_data

    # Append to CSV log
    with open("logs/trade_log.csv", "a") as log_file:
        log_file.write(
            f"{symbol},{action},{quantity},{entry_price},{exit_price},{trade_data['profit']}\n"
        )

    print(f"Trade logged: {trade_data}")
    return trade_data

def calculate_profit_loss(signal):
    """Calculate profit or loss for a trade."""
    symbol = signal.get("symbol")
    price = signal.get("price")

    if not symbol or not price:
        print("Invalid signal for P&L calculation. Missing symbol or price.")
        return None

    if symbol in TRADE_LOG:
        previous_trade = TRADE_LOG[symbol]
        if previous_trade["action"] != signal["action"]:  # Opposite action indicates closing trade
            pnl = (price - previous_trade["entry_price"]) * previous_trade["quantity"]
            pnl = pnl if previous_trade["action"] == "BUY" else -pnl
            print(f"Profit/Loss for {symbol}: {pnl:.2f}")
            logging.info(f"Profit/Loss for {symbol}: {pnl:.2f}")

            # Remove symbol from TRADE_LOG after calculating P&L
            del TRADE_LOG[symbol]
            return pnl
        else:
            print(f"No closing trade for {symbol} to calculate P&L.")
            return None
    else:
        print(f"No previous trade found for {symbol}.")
        return None
