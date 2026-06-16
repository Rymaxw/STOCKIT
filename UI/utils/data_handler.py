import pandas as pd
import numpy as np
import os
from datetime import datetime
import streamlit as st

try:
    from Utils.scoring import PengelolaDataSaham, PenilaiSaham
except ImportError:
    pass


class PengelolaDataSahamUI:

    def __init__(self, daftar_ticker: list):
        self.daftar_ticker = [t.strip() for t in daftar_ticker if t.strip()]
        self.folder_utama = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.folder_mentah = os.path.join(self.folder_utama, 'Data', 'Raw')

    def _muat_parquet(self, ticker: str) -> pd.DataFrame:
        lokasi_berkas = os.path.join(self.folder_mentah, f"{ticker}.parquet")
        if not os.path.exists(lokasi_berkas):
            return pd.DataFrame()

        df = pd.read_parquet(lokasi_berkas)
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        return df

    def _filter_rentang_waktu(self, df: pd.DataFrame, tanggal_mulai, tanggal_akhir) -> pd.DataFrame:
        masker = (df.index >= tanggal_mulai) & (df.index <= tanggal_akhir)
        return df.loc[masker]

    def ambil_data_historis(self, tanggal_mulai, tanggal_akhir) -> pd.DataFrame:
        if not self.daftar_ticker or not tanggal_mulai or not tanggal_akhir:
            return pd.DataFrame()

        tanggal_mulai = pd.to_datetime(tanggal_mulai)
        tanggal_akhir = pd.to_datetime(tanggal_akhir)

        kumpulan_data = list(filter(
            lambda df: df is not None,
            map(lambda ticker: self._proses_satu_ticker(ticker, tanggal_mulai, tanggal_akhir), self.daftar_ticker)
        ))

        if not kumpulan_data:
            return pd.DataFrame()

        df_gabungan = pd.concat(kumpulan_data, axis=1)
        return df_gabungan.ffill().bfill()

    def _proses_satu_ticker(self, ticker: str, tanggal_mulai, tanggal_akhir):
        try:
            df = self._muat_parquet(ticker)
            if df.empty:
                return None
            df_terfilter = self._filter_rentang_waktu(df, tanggal_mulai, tanggal_akhir)
            if df_terfilter.empty:
                return None
            return df_terfilter[['Close']].rename(columns={'Close': ticker})
        except Exception:
            return None

    @st.cache_data(ttl=3600)
    def ambil_saham_terbaik(_self) -> pd.DataFrame:
        try:
            pengelola = PengelolaDataSaham(folder_data=_self.folder_mentah)
            data_gabungan = pengelola.muat_semua_data()

            if data_gabungan.empty:
                return pd.DataFrame()

            penilai = PenilaiSaham()
            saham_terbaik = penilai.evaluasi_saham(data_gabungan)

            if saham_terbaik.empty:
                return pd.DataFrame()

            return _self._format_hasil_penilaian(saham_terbaik)

        except Exception:
            return pd.DataFrame()

    @st.cache_data(ttl=300)
    def ambil_saham_terbaik_live(_self) -> dict:
        try:
            from Utils.st_dataloader import baca_daftar_ticker
            lokasi_json = os.path.join(_self.folder_utama, 'Data', 'Raw', 'tickers_us.json')
            if os.path.exists(lokasi_json):
                daftar_saham = baca_daftar_ticker(lokasi_json)
            else:
                daftar_saham = [
                    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA',
                    'AVGO', 'AMD', 'ORCL', 'BRK-B', 'JPM', 'V', 'MA', 'BAC',
                    'LLY', 'UNH', 'JNJ', 'MRK', 'ABBV', 'WMT', 'PG', 'COST',
                    'HD', 'KO', 'PEP', 'CVX', 'XOM', 'CRM', 'NFLX'
                ]
            
            import yfinance as yf
            data_live = yf.download(daftar_saham, period="60d", progress=False)
            
            if data_live.empty:
                return {'tabel': pd.DataFrame(), 'historis': pd.DataFrame(), 'ohlcv': pd.DataFrame()}
            
            data_dict = {}
            for ticker in daftar_saham:
                if ticker in data_live['Close'].columns:
                    df_ticker = pd.DataFrame(data_live['Close'][ticker]).rename(columns={ticker: 'Close'})
                    df_ticker = df_ticker.dropna()
                    if not df_ticker.empty:
                        data_dict[ticker] = df_ticker
            
            if not data_dict:
                return {'tabel': pd.DataFrame(), 'historis': pd.DataFrame(), 'ohlcv': pd.DataFrame()}
            
            from Utils.scoring import PenilaiSaham
            penilai = PenilaiSaham()
            saham_terbaik = penilai.evaluasi_saham(data_dict)
            
            if saham_terbaik.empty:
                return {'tabel': pd.DataFrame(), 'historis': pd.DataFrame(), 'ohlcv': pd.DataFrame()}
            
            # Ambil data historis harga penutupan untuk sparkline
            df_historis = data_live['Close'].dropna(how='all')
            
            return {
                'tabel': _self._format_hasil_penilaian(saham_terbaik),
                'historis': df_historis,
                'ohlcv': data_live,
            }
        except Exception:
            return {'tabel': pd.DataFrame(), 'historis': pd.DataFrame(), 'ohlcv': pd.DataFrame()}


    @staticmethod
    def _format_hasil_penilaian(tabel: pd.DataFrame) -> pd.DataFrame:
        hasil = tabel.rename(columns={
            'Kode_Saham': 'Ticker',
            'Profit_30H': 'Return (%)',
            'Volatilitas': 'Risiko (%)',
            'Skor_Akhir': 'Skor'
        })

        hasil['Return (%)'] = (hasil['Return (%)'] * 100).round(2)
        hasil['Risiko (%)'] = (hasil['Risiko (%)'] * 100).round(2)
        hasil['Skor'] = (hasil['Skor'] * 100).round(1)

        # Tambah kolom harga dan perubahan harian jika tersedia dari scoring
        kolom_output = ['Ticker', 'Return (%)', 'Risiko (%)', 'Skor']
        if 'Harga_Terakhir' in hasil.columns:
            hasil['Harga'] = hasil['Harga_Terakhir'].round(2)
            kolom_output.append('Harga')
        if 'Perubahan_Harian' in hasil.columns:
            hasil['Perubahan Harian (%)'] = (hasil['Perubahan_Harian'] * 100).round(2)
            kolom_output.append('Perubahan Harian (%)')

        return hasil[kolom_output]