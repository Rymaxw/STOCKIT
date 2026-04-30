import pandas as pd
import numpy as np
from datetime import datetime

class StockDataHandler:
    def __init__(self, tickers: list):
        self.tickers = [t.strip() for t in tickers if t.strip()]

    def fetch_historical_data(self, start_date, end_date) -> pd.DataFrame:
        if not self.tickers or not start_date or not end_date:
            return pd.DataFrame()
            
        # Hitung jumlah hari untuk dummy data
        days = (end_date - start_date).days
        if days <= 0:
            days = 1 # Mencegah error jika tanggal sama
            
        # Generate dummy data dengan index berupa tanggal
        dates = pd.date_range(start=start_date, periods=days)
        data = np.random.randn(days, len(self.tickers))
        
        return pd.DataFrame(data, index=dates, columns=self.tickers)

    def get_top_performers(self) -> pd.DataFrame:
        data = {
            'Ticker': ['BBCA.JK', 'BMRI.JK', 'BREN.JK', 'AMMN.JK', 'TLKM.JK'],
            'Return (%)': [15.2, 12.8, 11.5, 10.1, 8.5],
            'Risk (%)': [5.1, 6.2, 8.5, 7.0, 4.5],
            'Skor': [92, 88, 81, 79, 75]
        }
        return pd.DataFrame(data)