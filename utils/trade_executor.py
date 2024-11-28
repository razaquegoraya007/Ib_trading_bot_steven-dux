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
            return

        print(f"Placing order: {action} {quantity} {symbol} at market price.")
        order = MarketOrder(action, quantity)
        trade = ib.placeOrder(contract, order)

        # Log trade details
        log_trade(symbol, action, quantity, price)

        print(f"Order placed: {trade}")

    except Exception as e:
        print(f"Error executing trade: {e}")
    finally:
        print("Disconnecting from IB Gateway after trade execution...")
        ib.disconnect()

def log_trade(symbol, action, quantity, price):
    """Log trade details."""
    global TRADE_LOG
    TRADE_LOG[symbol] = {
        "action": action,
        "price": price,
        "quantity": quantity,
    }

    # Log trade to CSV file
    with open("logs/trade_log.csv", "a") as log_file:
        log_file.write(f"{symbol},{action},{quantity},{price}\n")
    print(f"Trade logged: {symbol}, {action}, {quantity}, {price}")

def calculate_profit_loss(signal):
    """Calculate profit or loss for a trade."""
    symbol = signal.get("symbol")
    price = signal.get("price")

    if not symbol or not price:
        print("Invalid signal for P&L calculation. Missing symbol or price.")
        return

    if symbol in TRADE_LOG:
        previous_trade = TRADE_LOG[symbol]
        if previous_trade["action"] != signal["action"]:  # Opposite action indicates closing trade
            pnl = (price - previous_trade["price"]) * previous_trade["quantity"]
            pnl = pnl if previous_trade["action"] == "BUY" else -pnl
            print(f"Profit/Loss for {symbol}: {pnl:.2f}")
            logging.info(f"Profit/Loss for {symbol}: {pnl:.2f}")

            # Remove symbol from TRADE_LOG after calculating P&L
            del TRADE_LOG[symbol]
        else:
            print(f"No closing trade for {symbol} to calculate P&L.")
