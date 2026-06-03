import warnings
warnings.filterwarnings("ignore")
import json
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path


class PrediksiHargaSaham:
    """Memproyeksikan harga saham ke depan berdasarkan data historis dan metadata model."""

    PETA_FREKUENSI = {
        'mingguan': {'sufiks': '_mingguan.parquet', 'freq': 'W', 'label': '1 Minggu'},
        'bulanan': {'sufiks': '_bulanan.parquet', 'freq': 'M', 'label': '1 Bulan'},
        'tahunan': {'sufiks': '_tahunan.parquet', 'freq': 'Y', 'label': '1 Tahun'},
    }

    def __init__(self, folder_proyek: Path = None):
        if folder_proyek is None:
            folder_proyek = Path(__file__).resolve().parent.parent.parent
        self.folder_proyek = folder_proyek
        self.folder_processed = folder_proyek / 'Data' / 'Processed'
        self.folder_model = folder_proyek / 'Models'

    @st.cache_data(ttl=3600, show_spinner=False)
    def _muat_data_processed(_self, ticker: str, frekuensi: str) -> pd.DataFrame:
        info = _self.PETA_FREKUENSI[frekuensi]
        lokasi = _self.folder_processed / f"{ticker}{info['sufiks']}"
        if not lokasi.exists():
            return pd.DataFrame()

        df = pd.read_parquet(lokasi)
        if hasattr(df.index, 'tz') and df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        df = df.asfreq(info['freq'])
        df = df.ffill()
        return df

    @st.cache_data(ttl=3600, show_spinner=False)
    def _muat_metadata(_self, ticker: str, frekuensi: str) -> dict:
        folder = _self.folder_model / frekuensi.capitalize()
        lokasi = folder / f"{ticker}_metadata.json"
        if not lokasi.exists():
            return {}
        with open(lokasi, 'r') as f:
            return json.load(f)

    def _hitung_proyeksi(self, df: pd.DataFrame, horizon: int) -> dict:
        """Menghitung proyeksi harga berdasarkan rata-rata log return dan volatilitas."""
        if df.empty or 'Close' not in df.columns:
            return {'harga_sekarang': 0, 'prediksi': 0, 'optimis': 0, 'pesimis': 0, 'return_pct': 0}

        harga_terakhir = float(df['Close'].iloc[-1])
        log_return = np.log(df['Close'] / df['Close'].shift(1)).dropna()

        if len(log_return) < 5:
            return {'harga_sekarang': harga_terakhir, 'prediksi': harga_terakhir,
                    'optimis': harga_terakhir, 'pesimis': harga_terakhir, 'return_pct': 0}

        mu = float(log_return.mean())
        sigma = float(log_return.std())

        # Expected price = S0 * exp(mu * h)
        prediksi = harga_terakhir * np.exp(mu * horizon)
        # 1-sigma confidence band
        optimis = harga_terakhir * np.exp((mu + sigma) * horizon)
        pesimis = harga_terakhir * np.exp((mu - sigma) * horizon)

        return_pct = ((prediksi - harga_terakhir) / harga_terakhir) * 100

        return {
            'harga_sekarang': round(harga_terakhir, 2),
            'prediksi': round(prediksi, 2),
            'optimis': round(optimis, 2),
            'pesimis': round(pesimis, 2),
            'return_pct': round(return_pct, 2),
        }

    def prediksi_saham(self, ticker: str) -> dict:
        """Menghasilkan prediksi 1W, 1M, 1Y untuk satu saham."""
        hasil = {'ticker': ticker}

        # 1 Minggu periode
        df_w = self._muat_data_processed(ticker, 'mingguan')
        hasil['1W'] = self._hitung_proyeksi(df_w, horizon=1)
        meta_w = self._muat_metadata(ticker, 'mingguan')
        hasil['1W']['model'] = meta_w.get('model_terbaik', 'N/A')
        hasil['1W']['mae'] = self._ambil_mae(meta_w)

        # 1 Bulan periode
        df_m = self._muat_data_processed(ticker, 'bulanan')
        hasil['1M'] = self._hitung_proyeksi(df_m, horizon=1)
        meta_m = self._muat_metadata(ticker, 'bulanan')
        hasil['1M']['model'] = meta_m.get('model_terbaik', 'N/A')
        hasil['1M']['mae'] = self._ambil_mae(meta_m)

        # 1 Tahun periode
        df_y = self._muat_data_processed(ticker, 'tahunan')
        hasil['1Y'] = self._hitung_proyeksi(df_y, horizon=1)
        meta_y = self._muat_metadata(ticker, 'tahunan')
        hasil['1Y']['model'] = meta_y.get('model_terbaik', 'N/A')
        hasil['1Y']['mae'] = self._ambil_mae(meta_y)

        # Harga sekarang diambil dari data mingguan
        hasil['harga_sekarang'] = hasil['1W'].get('harga_sekarang', 0)

        return hasil

    @staticmethod
    def _ambil_mae(metadata: dict) -> float:
        metrik = metadata.get('metrik_top5', {})
        mae_dict = metrik.get('MAE', {})
        if mae_dict:
            return round(min(mae_dict.values()), 4)
        return 0.0


class PerbandinganInvestasi:
    """Membandingkan proyeksi investasi antar saham dengan budget tertentu."""

    def __init__(self, daftar_ticker: list, budget: float):
        self.daftar_ticker = daftar_ticker
        self.budget = budget
        self.engine = PrediksiHargaSaham()
        self._hasil_prediksi = {}

    def jalankan(self) -> dict:
        """Menjalankan prediksi untuk semua saham dan menghitung nilai investasi."""
        for ticker in self.daftar_ticker:
            pred = self.engine.prediksi_saham(ticker)
            self._hasil_prediksi[ticker] = pred
        return self._hasil_prediksi

    def buat_tabel_perbandingan(self, horizon: str = '1W') -> pd.DataFrame:
        """Menghasilkan tabel perbandingan investasi untuk horizon tertentu."""
        if not self._hasil_prediksi:
            self.jalankan()

        jumlah_saham = len(self.daftar_ticker)
        budget_per_saham = self.budget / jumlah_saham if jumlah_saham > 0 else 0

        rows = []
        for ticker in self.daftar_ticker:
            pred = self._hasil_prediksi.get(ticker, {})
            info = pred.get(horizon, {})
            harga_now = info.get('harga_sekarang', 0)
            harga_pred = info.get('prediksi', 0)
            return_pct = info.get('return_pct', 0)

            # Jumlah saham yang bisa dibeli
            jumlah_lembar = int(budget_per_saham / harga_now) if harga_now > 0 else 0
            nilai_awal = jumlah_lembar * harga_now
            nilai_prediksi = jumlah_lembar * harga_pred
            profit = nilai_prediksi - nilai_awal

            rows.append({
                'Ticker': ticker,
                'Harga Sekarang ($)': harga_now,
                f'Prediksi ({horizon})': harga_pred,
                'Return (%)': return_pct,
                'Lembar Saham': jumlah_lembar,
                'Nilai Awal ($)': round(nilai_awal, 2),
                'Nilai Prediksi ($)': round(nilai_prediksi, 2),
                'Profit ($)': round(profit, 2),
                'Model AI': info.get('model', 'N/A'),
            })

        return pd.DataFrame(rows)

    def buat_data_chart(self) -> pd.DataFrame:
        """Menghasilkan data untuk bar chart perbandingan return per horizon."""
        if not self._hasil_prediksi:
            self.jalankan()

        rows = []
        for ticker in self.daftar_ticker:
            pred = self._hasil_prediksi.get(ticker, {})
            rows.append({
                'Ticker': ticker,
                '1 Minggu (%)': pred.get('1W', {}).get('return_pct', 0),
                '1 Bulan (%)': pred.get('1M', {}).get('return_pct', 0),
                '1 Tahun (%)': pred.get('1Y', {}).get('return_pct', 0),
            })
        return pd.DataFrame(rows)
