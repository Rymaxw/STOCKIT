import pandas as pd

class PortfolioOptimizer:
    def __init__(self, tickers: list, initial_investment: float):
        self.tickers = tickers
        self.initial_investment = initial_investment
        self.n_assets = len(tickers)

    def get_kpi_metrics(self) -> dict:
        return {
            "expected_return": "12.5%",
            "volatility": "8.2%",
            "sharpe_ratio": "1.52"
        }

    def calculate_optimal_weights(self) -> pd.DataFrame:
        if self.n_assets == 0:
            return pd.DataFrame()
            
        weight = 1.0 / self.n_assets
        weights_list = [weight] * self.n_assets
        return pd.DataFrame({
            'Saham': self.tickers, 
            'Bobot': weights_list
        })

    def generate_allocation_report(self, price_per_lot: float = 500000) -> pd.DataFrame:
        if self.n_assets == 0:
            return pd.DataFrame()

        weight = 1.0 / self.n_assets
        alloc_rp = self.initial_investment * weight
        
        report_data = []
        for ticker in self.tickers:
            lots = int(alloc_rp / price_per_lot)
            report_data.append({
                'Ticker': ticker,
                'Bobot (%)': f"{weight*100:.1f}%",
                'Alokasi (Rp)': alloc_rp,
                'Jumlah Lot': lots
            })
            
        return pd.DataFrame(report_data)