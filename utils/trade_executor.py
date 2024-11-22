from ib_insync import MarketOrder, IB

def execute_trade(signal):
    """Execute trade based on the signal."""
    ib = IB()
    try:
        print("Connecting to IB Gateway for trade execution...")
        ib.connect("127.0.0.1", 4001, clientId=2)

        # Extract details from signal
        action = signal.get("action")
        symbol = signal.get("symbol")
        quantity = signal.get("quantity", 100)  # Default quantity if not provided
        contract = signal.get("contract")

        if not action or not symbol or not contract:
            print("Invalid signal. Missing action, symbol, or contract.")
            return

        print(f"Placing order: {action} {quantity} {symbol} at market price.")
        order = MarketOrder(action, quantity)
        trade = ib.placeOrder(contract, order)
        print(f"Order placed: {trade}")

    except Exception as e:
        print(f"Error executing trade: {e}")
    finally:
        print("Disconnecting from IB Gateway after trade execution...")
        ib.disconnect()
