import pandas as pd
# pyrefly: ignore [missing-import]
import yfinance as yf
import os
import concurrent.futures 
import time
import json

MAP_PERIODE = {
    "1 Tahun Terakhir": "1y",
    "3 Tahun Terakhir": "3y",
    "5 Tahun Terakhir": "5y",
    "10 Tahun Terakhir": "10y",
    "21 Tahun Terakhir": "21y",
}

MAP_FREKUENSI = {
    "Harian Daily": "1d",
    "Mingguan Weekly": "1wk",
    "Bulanan Monthly": "1mo"
}

class PengambilDataSaham:
    def ambil_data(self, kode_saham, periode, interval):
        try:
            saham = yf.Ticker(kode_saham)
            data_saham = saham.history(period=periode, interval=interval)
            if data_saham.empty:
                return None, "Data kosong"
            return data_saham, "Sukses"
        except Exception as e:
            return None, str(e)

class PemrosesData:
    def __init__(self):
        self.kolom_wajib = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.logika_agregasi = {
            'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'
        }

    def filter_kolom_wajib(self, data_saham):
        return data_saham[self.kolom_wajib].copy()

    def agregasi_waktu(self, data_ohlcv, frekuensi):
        kode_freq = {'mingguan': 'W', 'bulanan': 'ME', 'tahunan': 'YE'}[frekuensi]
        return data_ohlcv.resample(kode_freq).agg(self.logika_agregasi).dropna()

class ManajerPenyimpanan:
    def __init__(self, folder_proyek):
        self.sumber_data = os.path.join(folder_proyek, 'Data', 'Raw')
        self.folder_diproses = os.path.join(folder_proyek, 'Data', 'Processed')
        os.makedirs(self.sumber_data, exist_ok=True)
        os.makedirs(self.folder_diproses, exist_ok=True)

    def simpan_mentah(self, data_ohlcv, kode_saham):
        lokasi = os.path.join(self.sumber_data, f"{kode_saham}.parquet")
        data_ohlcv.to_parquet(lokasi)

    def simpan_agregasi(self, data_agregasi, kode_saham, frekuensi):
        lokasi = os.path.join(self.folder_diproses, f"{kode_saham}_{frekuensi}.parquet")
        data_agregasi.to_parquet(lokasi)

class OrkestratorPipeline:
    def __init__(self, pengambil, pemroses, manajer):
        self.pengambil = pengambil
        self.pemroses = pemroses
        self.manajer = manajer

    def proses_satu_saham(self, kode_saham, periode_yf, interval_yf):
        data_saham, pesan = self.pengambil.ambil_data(kode_saham, periode_yf, interval_yf)
        if data_saham is None:
            return kode_saham, False, pesan

        try:
            data_ohlcv = self.pemroses.filter_kolom_wajib(data_saham)
            self.manajer.simpan_mentah(data_ohlcv, kode_saham)
            for frekuensi in ['mingguan', 'bulanan', 'tahunan']:
                data_agregasi = self.pemroses.agregasi_waktu(data_ohlcv, frekuensi)
                self.manajer.simpan_agregasi(data_agregasi, kode_saham, frekuensi)
                
            return kode_saham, True, "Data Mentah & Diproses Berhasil Disimpan"
        except Exception as e:
            return kode_saham, False, f"Gagal saat memproses/menyimpan: {str(e)}"

    def jalankan_paralel(self, daftar_kode_saham, periode_antarmuka="21 Tahun Terakhir", frekuensi_antarmuka="Harian Daily"):
        periode_yf = MAP_PERIODE.get(periode_antarmuka, "21y")
        interval_yf = MAP_FREKUENSI.get(frekuensi_antarmuka, "1d")
        
        hasil_sukses = []
        hasil_gagal = []
        
        print(f"Memulai unduh data {len(daftar_kode_saham)} saham secara paralel\n")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as eksekutor:
            tugas_paralel = [
                eksekutor.submit(self.proses_satu_saham, kode_saham, periode_yf, interval_yf) 
                for kode_saham in daftar_kode_saham
            ]
            
            for tugas in concurrent.futures.as_completed(tugas_paralel):
                kode_saham, sukses, pesan = tugas.result()
                if sukses:
                    hasil_sukses.append(kode_saham)
                else:
                    hasil_gagal.append({kode_saham: pesan})
                    
        print(f"Sukses {len(hasil_sukses)} | Gagal {len(hasil_gagal)}")
        return hasil_sukses, hasil_gagal
if __name__ == "__main__":
    print("\n>>> MEMULAI PROSES PIPELINE <<<")
    folder_utama = os.path.dirname(os.path.abspath(__file__))
    folder_proyek = os.path.dirname(folder_utama)
    sumber_data = os.path.join(folder_proyek, 'Data', 'Raw')
    os.makedirs(sumber_data, exist_ok=True)
    lokasi_json = os.path.join(sumber_data, 'tickers_us.json')
    
    with open(lokasi_json, 'r') as berkas:
            data_json = json.load(berkas)        
    daftar_saham_tes = [item['yf_symbol'] for item in data_json['tickers']]
    print(f"Berhasil memuat {len(daftar_saham_tes)} kode saham dari JSON!")
    # Inisialisasi Class
    pengambil = PengambilDataSaham()
    pemroses = PemrosesData()
    manajer = ManajerPenyimpanan(folder_proyek)
    pipeline = OrkestratorPipeline(pengambil, pemroses, manajer)
    
    waktu_mulai = time.time()
    sukses, gagal = pipeline.jalankan_paralel(
        daftar_kode_saham=daftar_saham_tes, 
        periode_antarmuka="21 Tahun Terakhir", 
        frekuensi_antarmuka="Harian Daily"
    )
    print(f"Waktu Eksekusi {time.time() - waktu_mulai:.2f} detik\n")
    
    print(">>> INSPEKSI DATA PARQUET <<<")
    kode_saham_cek = sukses[0] if sukses else None
    
    if kode_saham_cek in sukses:
        lokasi_berkas = os.path.join(manajer.sumber_data, f"{kode_saham_cek}.parquet")
        data_inspeksi = pd.read_parquet(lokasi_berkas)
        
        print(f"Data {kode_saham_cek} berhasil dimuat dari: {lokasi_berkas}")
        print(f"Total baris: {len(data_inspeksi)}")
        print(f"\nPratinjau 5 data teratas {kode_saham_cek}:")
        print(data_inspeksi.head())
        print("\nCek Nilai Kosong (NaN):")
        print(data_inspeksi.isna().sum())
        
        print("\n" + "="*40)
        print(">>> VALIDASI BENTUK DATA AGREGASI <<<")
        print("="*40)
        
        for frekuensi, label in [('mingguan', 'MINGGUAN'), ('bulanan', 'BULANAN'), ('tahunan', 'TAHUNAN')]:
            lokasi_agregasi = os.path.join(manajer.folder_diproses, f"{kode_saham_cek}_{frekuensi}.parquet")
            if os.path.exists(lokasi_agregasi):
                data_agregasi = pd.read_parquet(lokasi_agregasi)
                print(f"\n[{label}] Total baris: {len(data_agregasi)} | Kolom: {len(data_agregasi.columns)}")
                print(data_agregasi.head(3))
            else:
                print(f"\n[{label}] Berkas tidak ditemukan: {lokasi_agregasi}")