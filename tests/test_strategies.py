import unittest
from strategies.bounce_short import BounceShortStrategy
from strategies.gap_up_short import gap_up_short_strategy

def test_gap_up_short_strategy():
    # Mock data
    mock_data = {
        "last_price": 105,
        "opening_price": 112,
        "high": 115,
        "volume": 1000000
    }
    result = gap_up_short_strategy("AAPL", mock_data)
    assert result is not None, "Gap-Up Short signal not triggered as expected"
    print("Gap-Up Short strategy test passed.")

if __name__ == "__main__":
    test_gap_up_short_strategy()
