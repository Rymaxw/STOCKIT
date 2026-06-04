import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import json
from Utils.data_pipeline import PengambilDataSaham, PemrosesData, ManajerPenyimpanan, OrkestratorPipeline

def main():
    print("=== PENGUJIAN INTEGRASI INDIKATOR TEKNIKAL ===")
    
    folder_utama = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Folder proyek: {folder_utama}")
    
    # Inisialisasi pipeline
    pengambil = PengambilDataSaham()
    pemroses = PemrosesData()
    manajer = ManajerPenyimpanan(folder_utama)
    pipeline = OrkestratorPipeline(pengambil, pemroses, manajer)
    
    # Ambil 1 saham untuk pengujian (misal: AAPL)
    ticker_tes = "AAPL"
    print(f"\n1. Mengunduh dan memproses data untuk {ticker_tes}...")
    
    kode, sukses, pesan = pipeline.proses_satu_saham(ticker_tes, "1y", "1d")
    print(f"Hasil proses: {kode} | Sukses: {sukses} | Pesan: {pesan}")
    
    if not sukses:
        print("Pengujian gagal karena unduhan data gagal.")
        return
        
    # Validasi file harian
    lokasi_harian = os.path.join(manajer.sumber_data, f"{ticker_tes}.parquet")
    df_harian = pd.read_parquet(lokasi_harian)
    
    print("\n2. Validasi Kolom Indikator pada Data Harian:")
    kolom_baru = [
        'MA5', 'MA20', 'MA50', 'RSI_14', 
        'MACD_Garis', 'MACD_Sinyal', 'MACD_Histogram', 
        'Bollinger_Atas', 'Bollinger_Tengah', 'Bollinger_Bawah', 
        'ATR_14', 'Volatilitas_30H'
    ]
    
    print(f"Total baris data harian: {len(df_harian)}")
    print("Pratinjau beberapa kolom indikator:")
    print(df_harian[['Close'] + kolom_baru].tail(5))
    
    # Periksa nilai NaN
    print("\nJumlah nilai kosong (NaN) di awal data (karena rolling window):")
    print(df_harian[kolom_baru].isna().sum())
    
    # Validasi data agregasi (misal mingguan)
    print("\n3. Validasi Kolom Indikator pada Data Mingguan:")
    lokasi_mingguan = os.path.join(manajer.folder_diproses, f"{ticker_tes}_mingguan.parquet")
    df_mingguan = pd.read_parquet(lokasi_mingguan)
    print(f"Total baris data mingguan: {len(df_mingguan)}")
    print(df_mingguan[['Close'] + kolom_baru].tail(5))
    
    print("\n=== PENGUJIAN SELESAI ===")

if __name__ == "__main__":
    main()
