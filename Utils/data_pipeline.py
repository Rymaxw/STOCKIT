import pandas as pd
# pyrefly: ignore [missing-import]
import yfinance as yf
import os
import concurrent.futures 
import time
import json
import warnings

warnings.filterwarnings('ignore')

class PengambilDataSaham:
    def ambil_data(self, kode_saham, periode="21y", interval="1d"):
        try:
            saham = yf.Ticker(kode_saham)
            data_saham = saham.history(period=periode, interval=interval, auto_adjust=True)
            if data_saham.empty:
                return None, "Data kosong dari YFinance"
            return data_saham, "Sukses"
        except Exception as e:
            return None, f"Error YFinance: {str(e)}"

class PembersihanData:
    def bersihkan_data(self, data_saham):
        df = data_saham.copy()
        
        if hasattr(df.index, 'tz'):
            df.index = df.index.tz_localize(None)
        
        kolom_wajib = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = df[kolom_wajib]

        df = df.ffill().dropna()

        df['Outlier_Volume'] = self._deteksi_outlier_iqr(df, 'Volume')
        
        return df

    def _deteksi_outlier_iqr(self, df, kolom):
        Q1 = df[kolom].quantile(0.25)
        Q3 = df[kolom].quantile(0.75)
        IQR = Q3 - Q1
        batas_atas = Q3 + 1.5 * IQR
        batas_bawah = Q1 - 1.5 * IQR
        return (df[kolom] < batas_bawah) | (df[kolom] > batas_atas)

class TransformasiData:
    def __init__(self):
        self.logika_agregasi = {
            'Open': 'first', 
            'High': 'max', 
            'Low': 'min', 
            'Close': 'last', 
            'Volume': 'sum',
            'Outlier_Volume': 'any' 
        }

    def agregasi_waktu(self, data_bersih, frekuensi):
        kode_freq = {'mingguan': 'W', 'bulanan': 'M', 'tahunan': 'Y'}[frekuensi]
        df_agregasi = data_bersih.resample(kode_freq).agg(self.logika_agregasi)
        return df_agregasi.dropna()

class ManajerPenyimpanan:
    def __init__(self, folder_proyek):
        self.folder_diproses = os.path.join(folder_proyek, 'Data', 'Processed')
        os.makedirs(self.folder_diproses, exist_ok=True)

    def simpan_harian_bersih(self, data, kode_saham):
        lokasi = os.path.join(self.folder_diproses, f"{kode_saham}_harian_clean.parquet")
        data.to_parquet(lokasi)

    def simpan_agregasi(self, data, kode_saham, frekuensi):
        lokasi = os.path.join(self.folder_diproses, f"{kode_saham}_{frekuensi}.parquet")
        data.to_parquet(lokasi)

class OrkestratorPipeline:
    def __init__(self, pengambil, pembersih, transformasi, manajer):
        self.pengambil = pengambil
        self.pembersih = pembersih
        self.transformasi = transformasi
        self.manajer = manajer

    def proses_satu_saham(self, kode_saham):
        data_saham, pesan = self.pengambil.ambil_data(kode_saham)
        if data_saham is None:
            return kode_saham, False, pesan

        try:
            data_bersih = self.pembersih.bersihkan_data(data_saham)
            
            self.manajer.simpan_harian_bersih(data_bersih, kode_saham)
            
            for frekuensi in ['mingguan', 'bulanan', 'tahunan']:
                data_agregasi = self.transformasi.agregasi_waktu(data_bersih, frekuensi)
                self.manajer.simpan_agregasi(data_agregasi, kode_saham, frekuensi)
                
            return kode_saham, True, "Sukses"
        except Exception as e:
            return kode_saham, False, f"Gagal: {str(e)}"

    def jalankan_paralel(self, daftar_kode_saham):
        hasil_sukses = []
        hasil_gagal = []
        
        print(f"Memulai Ekstraksi & Pembersihan Data untuk {len(daftar_kode_saham)} Saham...")
        print("-" * 50)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as eksekutor:
            tugas_paralel = [eksekutor.submit(self.proses_satu_saham, k) for k in daftar_kode_saham]
            for tugas in concurrent.futures.as_completed(tugas_paralel):
                kode_saham, sukses, pesan = tugas.result()
                if sukses:
                    hasil_sukses.append(kode_saham)
                    print(f"[✓] {kode_saham:5} | Berhasil disingkronkan")
                else:
                    hasil_gagal.append({kode_saham: pesan})
                    print(f"[✗] {kode_saham:5} | Gagal: {pesan}")
                    
        return hasil_sukses, hasil_gagal

if __name__ == "__main__":
    folder_utama = os.path.dirname(os.path.abspath(__file__))
    folder_proyek = os.path.dirname(folder_utama)
    lokasi_json = os.path.join(folder_proyek, 'Data', 'Raw', 'tickers_us.json')
    
    with open(lokasi_json, 'r') as berkas:
        data_json = json.load(berkas)
        
    daftar_saham = [item['yf_symbol'] for item in data_json['tickers'] if item['available']]
    
    pipeline = OrkestratorPipeline(
        PengambilDataSaham(),
        PembersihanData(),
        TransformasiData(),
        ManajerPenyimpanan(folder_proyek)
    )
    
    waktu_mulai = time.time()
    sukses, gagal = pipeline.jalankan_paralel(daftar_saham)
    
    print("-" * 50)
    print(f"Selesai! Sukses: {len(sukses)}, Gagal: {len(gagal)}")
    print(f"Waktu Eksekusi: {time.time() - waktu_mulai:.2f} detik")