import pandas as pd
import numpy as np


class OptimasiPortofolio:

    SUKU_BUNGA_BEBAS_RISIKO = 0.05
    HARI_PERDAGANGAN = 252

    def __init__(self, daftar_ticker: list, modal_awal: float):
        self.daftar_ticker = daftar_ticker
        self.modal_awal = modal_awal
        self.jumlah_aset = len(daftar_ticker)

        from utils.data_handler import PengelolaDataSahamUI
        from datetime import datetime, timedelta

        pengelola = PengelolaDataSahamUI(daftar_ticker)
        tanggal_akhir = datetime.today()
        tanggal_mulai = tanggal_akhir - timedelta(days=365)

        df = pengelola.ambil_data_historis(tanggal_mulai, tanggal_akhir)
        if not df.empty:
            self.daftar_ticker = list(df.columns)
            self.jumlah_aset = len(self.daftar_ticker)
        else:
            self.daftar_ticker = []
            self.jumlah_aset = 0

        self._inisialisasi_metrik(df)

    def _inisialisasi_metrik(self, df: pd.DataFrame):
        if df.empty:
            self.rata_rata_return = None
            self.matriks_kovarian = None
            self.metrik = self._metrik_kosong()
            return

        return_harian = df.pct_change().dropna()
        self.rata_rata_return = return_harian.mean()
        self.matriks_kovarian = return_harian.cov()
        bobot = np.ones(self.jumlah_aset) / self.jumlah_aset

        return_portofolio = np.sum(self.rata_rata_return * bobot) * self.HARI_PERDAGANGAN
        volatilitas = np.sqrt(np.dot(bobot.T, np.dot(self.matriks_kovarian, bobot))) * np.sqrt(self.HARI_PERDAGANGAN)
        rasio_sharpe = (return_portofolio - self.SUKU_BUNGA_BEBAS_RISIKO) / volatilitas if volatilitas != 0 else 0

        self.metrik = {
            "proyeksi_return": f"{(return_portofolio * 100):.2f}%",
            "volatilitas": f"{(volatilitas * 100):.2f}%",
            "rasio_sharpe": f"{rasio_sharpe:.2f}"
        }

    @staticmethod
    def _metrik_kosong() -> dict:
        return {
            "proyeksi_return": "N/A",
            "volatilitas": "N/A",
            "rasio_sharpe": "N/A"
        }

    def ambil_metrik_kpi(self) -> dict:
        return self.metrik

    def _hitung_bobot_invers_volatilitas(self) -> np.ndarray:
        if self.matriks_kovarian is None:
            return np.ones(self.jumlah_aset) / self.jumlah_aset

        volatilitas_per_aset = np.sqrt(np.diag(self.matriks_kovarian))
        if np.sum(volatilitas_per_aset) <= 0:
            return np.ones(self.jumlah_aset) / self.jumlah_aset

        invers_vol = 1.0 / volatilitas_per_aset
        return invers_vol / np.sum(invers_vol)

    def hitung_bobot_optimal(self) -> pd.DataFrame:
        if self.jumlah_aset == 0:
            return pd.DataFrame()

        daftar_bobot = self._hitung_bobot_invers_volatilitas()
        return pd.DataFrame({
            'Saham': self.daftar_ticker,
            'Bobot': daftar_bobot
        })

    def buat_laporan_alokasi(self, harga_per_lot: float = 500000) -> pd.DataFrame:
        if self.jumlah_aset == 0:
            return pd.DataFrame()

        df_bobot = self.hitung_bobot_optimal()

        data_laporan = list(map(
            lambda baris: self._hitung_alokasi_per_saham(baris[1], harga_per_lot),
            df_bobot.iterrows()
        ))

        return pd.DataFrame(data_laporan)

    def _hitung_alokasi_per_saham(self, baris: pd.Series, harga_per_lot: float) -> dict:
        bobot = baris['Bobot']
        alokasi_rp = self.modal_awal * bobot
        return {
            'Ticker': baris['Saham'],
            'Bobot (%)': f"{bobot * 100:.1f}%",
            'Alokasi (Rp)': alokasi_rp,
            'Jumlah Lot': int(alokasi_rp / harga_per_lot)
        }