from ib_insync import IB, Stock

def fetch_real_time_data(symbol):
    """Fetch real-time market data for the given symbol."""
    ib = IB()
    try:
        print("Connecting to IB Gateway...")
        ib.connect("127.0.0.1", 4001, clientId=1)
        contract = Stock(symbol, "SMART", "USD")
        ib.qualifyContracts(contract)

        print(f"Requesting market data for: {symbol}")
        ticker = ib.reqMktData(contract)
        ib.sleep(2)  # Wait for data to arrive

        # Fetch historical data for resistance levels and pre-market high
        print(f"Fetching historical data for resistance levels and pre-market high for: {symbol}")
        bars = ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr='1 D',
            barSizeSetting='1 min',
            whatToShow='TRADES',
            useRTH=False
        )

        pre_market_high = None
        for bar in bars:
            # Check if the bar is from the pre-market session
            if bar.date.hour < 9 or (bar.date.hour == 9 and bar.date.minute < 30):
                if pre_market_high is None or bar.high > pre_market_high:
                    pre_market_high = bar.high

        resistance_levels = sorted([bar.high for bar in bars], reverse=True)[:2]  # Top 2 resistance levels

        if ticker.last:
            print(f"Data received for {symbol}: Last price: {ticker.last}")
            return {
                "symbol": symbol,
                "last_price": ticker.last,
                "volume": ticker.volume,
                "bid": ticker.bid,
                "ask": ticker.ask,
                "previous_close": ticker.close,
                "opening_price": ticker.open,
                "pre_market_high": pre_market_high,  # Include pre-market high
                "resistance_levels": resistance_levels  # Include resistance levels
            }
        else:
            print(f"No data available for {symbol}.")
            return None
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None
    finally:
        print("Disconnecting from IB Gateway...")
        ib.disconnect()
