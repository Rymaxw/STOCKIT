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
    def _muat_data_processed(_self, kode_saham: str, frekuensi: str) -> pd.DataFrame:
        info = _self.PETA_FREKUENSI[frekuensi]
        lokasi = _self.folder_processed / f"{kode_saham}{info['sufiks']}"
        if not lokasi.exists():
            return pd.DataFrame()

        df = pd.read_parquet(lokasi)
        if hasattr(df.index, 'tz') and df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        df = df.asfreq(info['freq'])
        df = df.ffill()
        return df

    @st.cache_data(ttl=3600, show_spinner=False)
    def _muat_metadata(_self, kode_saham: str, frekuensi: str) -> dict:
        folder = _self.folder_model / frekuensi.capitalize()
        lokasi = folder / f"{kode_saham}_metadata.json"
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

        rata_rata = float(log_return.mean())
        simpangan = float(log_return.std())

        prediksi = harga_terakhir * np.exp(rata_rata * horizon)
        optimis = harga_terakhir * np.exp((rata_rata + simpangan) * horizon)
        pesimis = harga_terakhir * np.exp((rata_rata - simpangan) * horizon)

        return_pct = ((prediksi - harga_terakhir) / harga_terakhir) * 100

        return {
            'harga_sekarang': round(harga_terakhir, 2),
            'prediksi': round(prediksi, 2),
            'optimis': round(optimis, 2),
            'pesimis': round(pesimis, 2),
            'return_pct': round(return_pct, 2),
        }

    def prediksi_saham(self, kode_saham: str) -> dict:
        """Menghasilkan prediksi 1W, 1M, 1Y untuk satu saham."""
        hasil = {'kode_saham': kode_saham}

        # 1 Minggu periode
        df_w = self._muat_data_processed(kode_saham, 'mingguan')
        hasil['1W'] = self._hitung_proyeksi(df_w, horizon=1)
        meta_w = self._muat_metadata(kode_saham, 'mingguan')
        hasil['1W']['model'] = meta_w.get('model_terbaik', 'N/A')
        hasil['1W']['mae'] = self._ambil_mae(meta_w)

        # 1 Bulan periode
        df_m = self._muat_data_processed(kode_saham, 'bulanan')
        hasil['1M'] = self._hitung_proyeksi(df_m, horizon=1)
        meta_m = self._muat_metadata(kode_saham, 'bulanan')
        hasil['1M']['model'] = meta_m.get('model_terbaik', 'N/A')
        hasil['1M']['mae'] = self._ambil_mae(meta_m)

        # 1 Tahun periode
        df_y = self._muat_data_processed(kode_saham, 'tahunan')
        hasil['1Y'] = self._hitung_proyeksi(df_y, horizon=1)
        meta_y = self._muat_metadata(kode_saham, 'tahunan')
        hasil['1Y']['model'] = meta_y.get('model_terbaik', 'N/A')
        hasil['1Y']['mae'] = self._ambil_mae(meta_y)

        # Harga sekarang diambil dari data mingguan
        hasil['harga_sekarang'] = hasil['1W'].get('harga_sekarang', 0)

        return hasil

    @staticmethod
    def _ambil_mae(metadata: dict) -> float:
        metrik = metadata.get('metrik_top5', {})
        kamus_mae = metrik.get('MAE', {})
        if kamus_mae:
            return round(min(kamus_mae.values()), 4)
        return 0.0


class PerbandinganInvestasi:
    """Membandingkan proyeksi investasi antar saham dengan anggaran tertentu."""

    def __init__(self, daftar_kode_saham: list, anggaran: float):
        self.daftar_kode_saham = daftar_kode_saham
        self.anggaran = anggaran
        self.mesin = PrediksiHargaSaham()
        self._hasil_prediksi = {}

    def jalankan(self) -> dict:
        """Menjalankan prediksi untuk semua saham dan menghitung nilai investasi."""
        for kode_saham in self.daftar_kode_saham:
            prediksi_data = self.mesin.prediksi_saham(kode_saham)
            self._hasil_prediksi[kode_saham] = prediksi_data
        return self._hasil_prediksi

    def buat_tabel_perbandingan(self, horizon: str = '1W') -> pd.DataFrame:
        """Menghasilkan tabel perbandingan investasi untuk horizon tertentu."""
        if not self._hasil_prediksi:
            self.jalankan()

        jumlah_saham = len(self.daftar_kode_saham)
        anggaran_per_saham = self.anggaran / jumlah_saham if jumlah_saham > 0 else 0

        baris = []
        for kode_saham in self.daftar_kode_saham:
            prediksi_data = self._hasil_prediksi.get(kode_saham, {})
            rincian = prediksi_data.get(cakrawala, {})
            harga_kini = rincian.get('harga_sekarang', 0)
            harga_prediksi = rincian.get('prediksi', 0)
            persen_imbal_hasil = rincian.get('persen_imbal_hasil', 0)

            jumlah_lembar = int(anggaran_per_saham / harga_kini) if harga_kini > 0 else 0
            nilai_awal = jumlah_lembar * harga_kini
            nilai_prediksi = jumlah_lembar * harga_prediksi
            keuntungan = nilai_prediksi - nilai_awal

            baris.append({
                'Kode Saham': kode_saham,
                'Harga Sekarang ($)': harga_kini,
                f'Prediksi ({cakrawala})': harga_prediksi,
                'Imbal Hasil (%)': persen_imbal_hasil,
                'Lembar Saham': jumlah_lembar,
                'Nilai Awal ($)': round(nilai_awal, 2),
                'Nilai Prediksi ($)': round(nilai_prediksi, 2),
                'Keuntungan ($)': round(keuntungan, 2),
                'Model AI': rincian.get('model', 'N/A'),
            })

        return pd.DataFrame(baris)

    def buat_data_chart(self) -> pd.DataFrame:
        """Menghasilkan data untuk bar chart perbandingan return per horizon."""
        if not self._hasil_prediksi:
            self.jalankan()

        baris = []
        for kode_saham in self.daftar_kode_saham:
            prediksi_data = self._hasil_prediksi.get(kode_saham, {})
            baris.append({
                'Kode Saham': kode_saham,
                '1 Minggu (%)': prediksi_data.get('1W', {}).get('persen_imbal_hasil', 0),
                '1 Bulan (%)': prediksi_data.get('1M', {}).get('persen_imbal_hasil', 0),
                '1 Tahun (%)': prediksi_data.get('1Y', {}).get('persen_imbal_hasil', 0),
            })
        return pd.DataFrame(baris)
