import warnings
warnings.filterwarnings("ignore")

import json
import numpy as np
import pandas as pd
from pathlib import Path


class PrediksiHargaSaham:
    """Memproyeksikan harga saham ke depan menggunakan model AI PyCaret yang sudah dilatih."""

    PETA_FREKUENSI = {
        'mingguan': {'sufiks': '_mingguan.parquet', 'freq': 'W', 'label': '1 Minggu', 'horizon': 4},
        'bulanan': {'sufiks': '_bulanan.parquet', 'freq': 'M', 'label': '1 Bulan', 'horizon': 12},
        'tahunan': {'sufiks': '_tahunan.parquet', 'freq': 'Y', 'label': '1 Tahun', 'horizon': 1},
    }

    def __init__(self, folder_proyek: Path = None):
        if folder_proyek is None:
            folder_proyek = Path(__file__).resolve().parent.parent.parent
        self.folder_proyek = folder_proyek
        self.folder_processed = folder_proyek / 'Data' / 'Processed'
        self.folder_model = folder_proyek / 'Models'
        self._cache_model = {}

    # ── Data loading ──────────────────────────────────────────────

    def _muat_data_processed(self, ticker: str, frekuensi: str) -> pd.DataFrame:
        info = self.PETA_FREKUENSI[frekuensi]
        lokasi = self.folder_processed / f"{ticker}{info['sufiks']}"
        if not lokasi.exists():
            return pd.DataFrame()

        df = pd.read_parquet(lokasi)
        if hasattr(df.index, 'tz') and df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        df = df.asfreq(info['freq'])
        df = df.ffill()
        return df

    def _muat_metadata(self, ticker: str, frekuensi: str) -> dict:
        folder = self.folder_model / frekuensi.capitalize()
        lokasi = folder / f"{ticker}_metadata.json"
        if not lokasi.exists():
            return {}
        with open(lokasi, 'r') as f:
            return json.load(f)

    def _muat_model_ai(self, ticker: str, frekuensi: str):
        """Memuat model PyCaret yang sudah dilatih dari file .pkl."""
        cache_key = f"{ticker}_{frekuensi}"
        if cache_key in self._cache_model:
            return self._cache_model[cache_key]

        folder = self.folder_model / frekuensi.capitalize()
        lokasi_model = folder / f"{ticker}_model_{frekuensi}"

        # PyCaret menyimpan tanpa ekstensi, tapi file aslinya .pkl
        if not (lokasi_model.with_suffix('.pkl')).exists():
            return None

        try:
            from pycaret.time_series import load_model
            model = load_model(str(lokasi_model), verbose=False)
            self._cache_model[cache_key] = model
            return model
        except Exception:
            return None

    # ── Projection engine (AI-powered) ─────────────────────────────

    def _hitung_proyeksi_ai(self, df: pd.DataFrame, ticker: str, frekuensi: str) -> dict:
        """Menghitung proyeksi harga menggunakan model AI PyCaret."""
        if df.empty or 'Close' not in df.columns:
            return {'harga_sekarang': 0, 'prediksi': 0, 'optimis': 0, 'pesimis': 0,
                    'return_pct': 0, 'metode': 'N/A'}

        harga_terakhir = float(df['Close'].iloc[-1])
        info = self.PETA_FREKUENSI[frekuensi]

        # Coba gunakan model AI terlebih dahulu
        model = self._muat_model_ai(ticker, frekuensi)
        if model is not None:
            try:
                prediksi_log_return = model.predict()
                if isinstance(prediksi_log_return, pd.DataFrame):
                    prediksi_log_return = prediksi_log_return.iloc[:, 0]

                # Ambil prediksi kumulatif log return
                kumulatif_return = float(prediksi_log_return.sum())
                prediksi_harga = harga_terakhir * np.exp(kumulatif_return)

                # Hitung confidence band dari volatilitas historis
                log_return_hist = np.log(df['Close'] / df['Close'].shift(1)).dropna()
                sigma = float(log_return_hist.std()) if len(log_return_hist) > 5 else 0.02
                horizon = info['horizon']

                optimis = harga_terakhir * np.exp(kumulatif_return + sigma * np.sqrt(horizon))
                pesimis = harga_terakhir * np.exp(kumulatif_return - sigma * np.sqrt(horizon))

                return_pct = ((prediksi_harga - harga_terakhir) / harga_terakhir) * 100

                return {
                    'harga_sekarang': round(harga_terakhir, 2),
                    'prediksi': round(prediksi_harga, 2),
                    'optimis': round(optimis, 2),
                    'pesimis': round(pesimis, 2),
                    'return_pct': round(return_pct, 2),
                    'metode': 'AI Model',
                }
            except Exception:
                pass  # Fallback ke metode statistik

        # Fallback: metode statistik (log return rata-rata)
        return self._hitung_proyeksi_statistik(df, info['horizon'])

    def _hitung_proyeksi_statistik(self, df: pd.DataFrame, horizon: int) -> dict:
        """Fallback: proyeksi berdasarkan rata-rata log return dan volatilitas."""
        if df.empty or 'Close' not in df.columns:
            return {'harga_sekarang': 0, 'prediksi': 0, 'optimis': 0, 'pesimis': 0,
                    'return_pct': 0, 'metode': 'Statistik'}

        harga_terakhir = float(df['Close'].iloc[-1])
        log_return = np.log(df['Close'] / df['Close'].shift(1)).dropna()

        if len(log_return) < 5:
            return {'harga_sekarang': harga_terakhir, 'prediksi': harga_terakhir,
                    'optimis': harga_terakhir, 'pesimis': harga_terakhir,
                    'return_pct': 0, 'metode': 'Statistik'}

        mu = float(log_return.mean())
        sigma = float(log_return.std())

        prediksi = harga_terakhir * np.exp(mu * horizon)
        optimis = harga_terakhir * np.exp((mu + sigma) * horizon)
        pesimis = harga_terakhir * np.exp((mu - sigma) * horizon)

        return_pct = ((prediksi - harga_terakhir) / harga_terakhir) * 100

        return {
            'harga_sekarang': round(harga_terakhir, 2),
            'prediksi': round(prediksi, 2),
            'optimis': round(optimis, 2),
            'pesimis': round(pesimis, 2),
            'return_pct': round(return_pct, 2),
            'metode': 'Statistik',
        }

    def prediksi_saham(self, ticker: str) -> dict:
        """Menghasilkan prediksi 1W, 1M, 1Y untuk satu saham menggunakan model AI."""
        hasil = {'ticker': ticker}

        # 1 Minggu → data mingguan
        df_w = self._muat_data_processed(ticker, 'mingguan')
        hasil['1W'] = self._hitung_proyeksi_ai(df_w, ticker, 'mingguan')
        meta_w = self._muat_metadata(ticker, 'mingguan')
        hasil['1W']['model'] = self._ambil_nama_model(meta_w)
        hasil['1W']['mae'] = self._ambil_mae(meta_w)

        # 1 Bulan → data bulanan
        df_m = self._muat_data_processed(ticker, 'bulanan')
        hasil['1M'] = self._hitung_proyeksi_ai(df_m, ticker, 'bulanan')
        meta_m = self._muat_metadata(ticker, 'bulanan')
        hasil['1M']['model'] = self._ambil_nama_model(meta_m)
        hasil['1M']['mae'] = self._ambil_mae(meta_m)

        # 1 Tahun → data tahunan
        df_y = self._muat_data_processed(ticker, 'tahunan')
        hasil['1Y'] = self._hitung_proyeksi_ai(df_y, ticker, 'tahunan')
        meta_y = self._muat_metadata(ticker, 'tahunan')
        hasil['1Y']['model'] = self._ambil_nama_model(meta_y)
        hasil['1Y']['mae'] = self._ambil_mae(meta_y)

        # Harga sekarang diambil dari data mingguan (paling up-to-date)
        hasil['harga_sekarang'] = hasil['1W'].get('harga_sekarang', 0)

        return hasil

    @staticmethod
    def _ambil_mae(metadata: dict) -> float:
        metrik = metadata.get('metrik_top5', {})
        mae_dict = metrik.get('MAE', {})
        if mae_dict:
            return round(min(mae_dict.values()), 4)
        return 0.0

    @staticmethod
    def _ambil_nama_model(metadata: dict) -> str:
        """Mengambil nama model yang readable dari metadata."""
        metrik = metadata.get('metrik_top5', {})
        model_dict = metrik.get('Model', {})
        if model_dict:
            # Ambil nama model pertama (yang terbaik)
            return list(model_dict.values())[0]
        return metadata.get('model_terbaik', 'N/A')


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
            metode = info.get('metode', 'N/A')

            # Jumlah saham yang bisa dibeli
            jumlah_lembar = int(budget_per_saham / harga_now) if harga_now > 0 else 0
            nilai_awal = jumlah_lembar * harga_now
            nilai_prediksi = jumlah_lembar * harga_pred
            profit = nilai_prediksi - nilai_awal

            rows.append({
                'Ticker': ticker,
                'Harga Sekarang (Rp)': harga_now,
                f'Prediksi ({horizon})': harga_pred,
                'Return (%)': return_pct,
                'Lembar Saham': jumlah_lembar,
                'Nilai Awal (Rp)': round(nilai_awal, 2),
                'Nilai Prediksi (Rp)': round(nilai_prediksi, 2),
                'Profit (Rp)': round(profit, 2),
                'Metode': metode,
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
