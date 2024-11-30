from ib_insync import IB, Stock, ScannerSubscription
import math

def fetch_all_stocks():
    """Fetch all available stocks dynamically."""
    ib = IB()
    try:
        print("Connecting to IB Gateway...")
        ib.connect("127.0.0.1", 4001, clientId=3)

        print("Fetching all available stock symbols...")
        scanner = ScannerSubscription(
            instrument='STK',  # Stock instrument
            locationCode='STK.US.MAJOR',  # Major US stock markets
            scanCode='TOP_PERC_GAIN'  # Top percent gainers
        )

        results = ib.reqScannerData(scanner)
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

        print(f"Fetching historical data for pre-market high for: {symbol}")
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
            if bar.date.hour < 9 or (bar.date.hour == 9 and bar.date.minute < 30):
                if pre_market_high is None or bar.high > pre_market_high:
                    pre_market_high = bar.high

        resistance_levels = sorted([bar.high for bar in bars if not math.isnan(bar.high)], reverse=True)[:2]

        if not math.isnan(ticker.last):
            print(f"Data received for {symbol}: Last price: {ticker.last}")
            return {
                "symbol": symbol,
                "last_price": ticker.last,
                "volume": ticker.volume,
                "bid": ticker.bid,
                "ask": ticker.ask,
                "previous_close": ticker.close,
                "opening_price": ticker.open,
                "pre_market_high": pre_market_high,
                "resistance_levels": resistance_levels
            }
        else:
            print(f"No valid last price for {symbol}.")
            return None

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

    finally:
        print("Disconnecting from IB Gateway...")
        ib.disconnect()
