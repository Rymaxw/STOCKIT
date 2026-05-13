import os
import json
import warnings
import time
import numpy as np
import pandas as pd
from pathlib import Path
from dataclasses import dataclass, asdict
from pycaret.time_series import (
    setup,
    compare_models,
    pull,
    save_model,
)

warnings.filterwarnings('ignore')


@dataclass
class KonfigurasiWaktu:
    nama: str
    sufiks_berkas: str
    frekuensi_pandas: str
    horizon_prediksi: int
    periode_musiman: int
    ukuran_training: int
    jumlah_fold: int


DAFTAR_KONFIGURASI = {
    'mingguan': KonfigurasiWaktu(
        nama='mingguan',
        sufiks_berkas='_mingguan.parquet',
        frekuensi_pandas='W',
        horizon_prediksi=4,
        periode_musiman=52,
        ukuran_training=780,
        jumlah_fold=3,
    ),
    'bulanan': KonfigurasiWaktu(
        nama='bulanan',
        sufiks_berkas='_bulanan.parquet',
        frekuensi_pandas='M',
        horizon_prediksi=12,
        periode_musiman=12,
        ukuran_training=180,
        jumlah_fold=5,
    ),
    'tahunan': KonfigurasiWaktu(
        nama='tahunan',
        sufiks_berkas='_tahunan.parquet',
        frekuensi_pandas='Y',
        horizon_prediksi=1,
        periode_musiman=1,
        ukuran_training=15,
        jumlah_fold=2,
    ),
}


class PemuatDataModel:
    def __init__(self, folder_diproses: Path):
        self.folder_diproses = folder_diproses

    def muat_dan_siapkan(self, kode_saham: str, konfigurasi: KonfigurasiWaktu) -> pd.DataFrame:
        lokasi_berkas = self.folder_diproses / f"{kode_saham}{konfigurasi.sufiks_berkas}"

        if not lokasi_berkas.exists():
            raise FileNotFoundError(f"File tidak ditemukan: {lokasi_berkas}")

        df = pd.read_parquet(lokasi_berkas)

        if hasattr(df.index, 'tz') and df.index.tz is not None:
            df.index = df.index.tz_localize(None)

        df = df.asfreq(konfigurasi.frekuensi_pandas)
        df = df.ffill()

        df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
        df = df.dropna(subset=['Log_Return'])

        return df

    def potong_data(self, df: pd.DataFrame, konfigurasi: KonfigurasiWaktu) -> pd.DataFrame:
        jumlah_potong = konfigurasi.ukuran_training + konfigurasi.horizon_prediksi
        if len(df) > jumlah_potong:
            return df.tail(jumlah_potong)
        return df


class PelatihModelPyCaret:
    def __init__(self):
        self.model_terbaik = None
        self.tabel_metrik = None

    def jalankan_setup(self, data: pd.DataFrame, konfigurasi: KonfigurasiWaktu):
        param_musiman = konfigurasi.periode_musiman if konfigurasi.periode_musiman > 1 else 1
        setup(
            data=data[['Log_Return']],
            fh=konfigurasi.horizon_prediksi,
            fold=konfigurasi.jumlah_fold,
            fold_strategy='sliding',
            seasonal_period=param_musiman,
            session_id=123,
            verbose=False,
        )
        return self

    def cari_model_terbaik(self):
        self.model_terbaik = compare_models(sort='MAE')
        self.tabel_metrik = pull()
        return self

    def simpan_model(self, lokasi_output: Path):
        save_model(self.model_terbaik, str(lokasi_output))
        return self


class OrkestratorPelatihan:
    def __init__(self, folder_proyek: Path):
        self.folder_proyek = folder_proyek
        self.folder_data = folder_proyek / 'Data' / 'Processed'
        self.folder_model = folder_proyek / 'Models'
        self.pemuat = PemuatDataModel(self.folder_data)

    def _siapkan_folder_model(self, nama_frekuensi: str) -> Path:
        folder = self.folder_model / nama_frekuensi.capitalize()
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def latih_satu_saham(self, kode_saham: str, konfigurasi: KonfigurasiWaktu):
        try:
            df = self.pemuat.muat_dan_siapkan(kode_saham, konfigurasi)
            df_potong = self.pemuat.potong_data(df, konfigurasi)

            minimal_baris = konfigurasi.horizon_prediksi * 3
            if len(df_potong) < minimal_baris:
                return kode_saham, False, f"Data terlalu sedikit ({len(df_potong)} baris, butuh minimal {minimal_baris})"

            harga_terakhir = float(df['Close'].iloc[-1])

            pelatih = PelatihModelPyCaret()
            pelatih.jalankan_setup(df_potong, konfigurasi)
            pelatih.cari_model_terbaik()

            folder_output = self._siapkan_folder_model(konfigurasi.nama)
            lokasi_model = folder_output / f"{kode_saham}_model_{konfigurasi.nama}"
            pelatih.simpan_model(lokasi_model)

            metadata = {
                'kode_saham': kode_saham,
                'frekuensi': konfigurasi.nama,
                'harga_terakhir': harga_terakhir,
                'jumlah_data_training': len(df_potong),
                'model_terbaik': str(type(pelatih.model_terbaik).__name__),
                'metrik_top5': pelatih.tabel_metrik.head(5).to_dict() if pelatih.tabel_metrik is not None else {},
            }

            lokasi_metadata = folder_output / f"{kode_saham}_metadata.json"
            with open(lokasi_metadata, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)

            return kode_saham, True, f"Model: {metadata['model_terbaik']}"

        except Exception as e:
            return kode_saham, False, str(e)

    def latih_semua_saham(self, daftar_saham: list, frekuensi: str):
        konfigurasi = DAFTAR_KONFIGURASI[frekuensi]

        print(f"\n{'='*60}")
        print(f"  PELATIHAN MODEL - {konfigurasi.nama.upper()}")
        print(f"  Horizon: {konfigurasi.horizon_prediksi} | Fold: {konfigurasi.jumlah_fold}")
        print(f"  Jumlah Saham: {len(daftar_saham)}")
        print(f"{'='*60}\n")

        hasil_sukses = []
        hasil_gagal = []

        for i, kode_saham in enumerate(daftar_saham, 1):
            print(f"[{i}/{len(daftar_saham)}] Melatih {kode_saham}...", end=" ", flush=True)
            waktu_mulai = time.time()

            kode, sukses, pesan = self.latih_satu_saham(kode_saham, konfigurasi)
            durasi = time.time() - waktu_mulai

            if sukses:
                hasil_sukses.append(kode)
                print(f"OK ({durasi:.1f}s) | {pesan}")
            else:
                hasil_gagal.append({kode: pesan})
                print(f"GAGAL ({durasi:.1f}s) | {pesan}")

        print(f"\n{'='*60}")
        print(f"  RINGKASAN: Sukses {len(hasil_sukses)} | Gagal {len(hasil_gagal)}")
        print(f"{'='*60}")

        return hasil_sukses, hasil_gagal


if __name__ == "__main__":
    folder_proyek = Path(__file__).resolve().parent.parent
    lokasi_json = folder_proyek / 'Data' / 'Raw' / 'tickers_us.json'

    with open(lokasi_json, 'r') as f:
        data_json = json.load(f)

    daftar_saham = [t['ticker'] for t in data_json['tickers'] if t['available']]

    orkestrator = OrkestratorPelatihan(folder_proyek)

    waktu_total = time.time()
    
    print("\n[INFO] Memulai proses pelatih model TAHUNAN...")
    sukses_tahunan, gagal_tahunan = orkestrator.latih_semua_saham(daftar_saham, frekuensi='tahunan')
    
    print("\n[INFO] Memulai proses pelatih model BULANAN...")
    sukses_bulanan, gagal_bulanan = orkestrator.latih_semua_saham(daftar_saham, frekuensi='bulanan')
    
    print("\n[INFO] Memulai proses pelatih model MINGGUAN...")
    sukses_mingguan, gagal_mingguan = orkestrator.latih_semua_saham(daftar_saham, frekuensi='mingguan')
        
    print(f"\nTotal Waktu Seluruh Pelatihan (3 Frekuensi): {time.time() - waktu_total:.1f} detik")
