import pandas as pd

class PerformanceMetrics:
    def __init__(self):
        self.equity_curve = pd.Series(dtype='float64')

    def update_equity_curve(self, value):
        self.equity_curve = self.equity_curve.append(pd.Series([value]))

    def calculate_sharpe_ratio(self, risk_free_rate=0.01):
        returns = self.equity_curve.pct_change().dropna()
        mean_return = returns.mean()
        std_return = returns.std()
        sharpe_ratio = (mean_return - risk_free_rate) / std_return
        return sharpe_ratio

    def calculate_max_drawdown(self):
        running_max = self.equity_curve.cummax()
        drawdown = self.equity_curve / running_max - 1
        max_drawdown = drawdown.min()
        return max_drawdown
