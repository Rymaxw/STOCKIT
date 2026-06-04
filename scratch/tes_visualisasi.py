import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from Utils.candlestick import muat_data_saham, buat_grafik_candlestick

def main():
    print("=== PENGUJIAN VISUALISASI CANDLESTICK ===")
    
    # Muat data saham GOOGL yang sudah diunduh
    print("Memuat data saham GOOGL...")
    data_dict = muat_data_saham(["GOOGL"], periode="1y")
    df = data_dict["GOOGL"]
    
    print(f"Bentuk data: {df.shape}")
    print("Membuat grafik dengan semua indikator teknikal...")
    
    fig = buat_grafik_candlestick(
        df,
        "GOOGL",
        "Google Inc. - Semua Indikator",
        tampilkan_ma5=True,
        tampilkan_ma20=True,
        tampilkan_ma50=True,
        tampilkan_ma200=True,
        tampilkan_bollinger=True,
        tampilkan_rsi=True,
        tampilkan_macd=True,
        tampilkan_atr=True,
        tampilkan_volatilitas=True
    )
    
    # Simpan plot ke file HTML sementara untuk memastikan tidak ada error pembuatan grafik
    lokasi_html = "scratch/test_plot.html"
    fig.write_html(lokasi_html)
    print(f"Grafik sukses ditulis ke: {lokasi_html}")
    print("=== PENGUJIAN SELESAI ===")

if __name__ == "__main__":
    main()
