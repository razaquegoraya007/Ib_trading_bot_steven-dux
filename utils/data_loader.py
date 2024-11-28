from ib_insync import IB, Stock, ScannerSubscription

def fetch_all_stocks():
    """Fetch all available stocks dynamically."""
    ib = IB()
    try:
        print("Connecting to IB Gateway...")
        ib.connect("127.0.0.1", 4001, clientId=3)

        # Create a scanner subscription for stocks
        print("Fetching all available stock symbols...")
        scanner = ScannerSubscription(
            instrument='STK',  # Stock instrument
            locationCode='STK.US.MAJOR',  # Major US stock markets
            scanCode='TOP_PERC_GAIN'  # Top percent gainers
        )

        results = ib.reqScannerData(scanner)

        # Extract stock symbols from scanner results
        stocks = [item.contractDetails.contract.symbol for item in results]
        print(f"Fetched {len(stocks)} stocks.")
        return stocks

    except Exception as e:
        print(f"Error fetching all stocks: {e}")
        return []

    finally:
        print("Disconnecting from IB Gateway...")
        ib.disconnect()


def fetch_real_time_data(symbol):
    """Fetch real-time market data for a given stock symbol."""
    ib = IB()
    try:
        print("Connecting to IB Gateway...")
        ib.connect("127.0.0.1", 4001, clientId=1)
        contract = Stock(symbol, "SMART", "USD")
        ib.qualifyContracts(contract)

        print(f"Requesting market data for: {symbol}")
        ticker = ib.reqMktData(contract)
        ib.sleep(2)  # Wait for data to arrive

        # Fallback: Fetch historical price if last_price is invalid
        if ticker.last is None or str(ticker.last).lower() == "nan":
            print(f"Invalid or missing last price for {symbol}. Attempting fallback...")
            bars = ib.reqHistoricalData(
                contract,
                endDateTime='',
                durationStr='1 D',
                barSizeSetting='5 mins',
                whatToShow='TRADES',
                useRTH=True
            )
            if bars:
                last_price = bars[-1].close  # Use the most recent close price as a fallback
                print(f"Fallback last price for {symbol}: {last_price}")
            else:
                print(f"Fallback failed for {symbol}. Skipping...")
                return None
        else:
            last_price = ticker.last

        print(f"Data received for {symbol}: Last price: {last_price}")
        return {
            "symbol": symbol,
            "last_price": last_price,
            "volume": ticker.volume,
            "bid": ticker.bid,
            "ask": ticker.ask,
            "previous_close": ticker.close,
            "opening_price": ticker.open,
            "pre_market_high": None,  # You can add additional logic here if needed
            "resistance_levels": []
        }

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

    finally:
        print("Disconnecting from IB Gateway...")
        ib.disconnect()
