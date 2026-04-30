import pandas as pd
import yfinance as yf
import os
import concurrent.futures 
import time
import json

MAP_PERIODE = {
    "1 Tahun Terakhir": "1y",
    "3 Tahun Terakhir": "3y",
    "5 Tahun Terakhir": "5y",
    "Maksimal": "max"
}

MAP_FREKUENSI = {
    "Harian Daily": "1d",
    "Mingguan Weekly": "1wk",
    "Bulanan Monthly": "1mo"
}

def simpan_satu_saham(ticker, yf_period, yf_interval):
    try:
        saham = yf.Ticker(ticker)
        df = saham.history(period=yf_period, interval=yf_interval)
        
        if df.empty:
            return ticker, False, "Data kosong"
            
        kolom_wajib = ['Open', 'High', 'Low', 'Close', 'Volume']
        df_ohlcv = df[kolom_wajib]
        
      
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        raw_dir = os.path.join(project_dir, 'Data', 'Raw')
        os.makedirs(raw_dir, exist_ok=True)
        filepath = os.path.join(raw_dir, f"{ticker}.parquet")
        df_ohlcv.to_parquet(filepath)
        
        return ticker, True, filepath
        
    except Exception as e:
        return ticker, False, str(e)

def uji_tarik_data_saham(daftar_ticker, ui_periode="1 Tahun Terakhir", ui_frekuensi="Harian Daily"):
    yf_period = MAP_PERIODE.get(ui_periode, "1y")
    yf_interval = MAP_FREKUENSI.get(ui_frekuensi, "1d")
    
    hasil_sukses = []
    hasil_gagal = []
    
    print(f"Memulai pull {len(daftar_ticker)} saham secara paralel\n")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(simpan_satu_saham, ticker, yf_period, yf_interval) 
            for ticker in daftar_ticker
        ]
        
        for future in concurrent.futures.as_completed(futures):
            ticker, sukses, info = future.result()
            
            if sukses:
                hasil_sukses.append(ticker)
            else:
                hasil_gagal.append({ticker: info})
                
    print(f"Sukses {len(hasil_sukses)} | Gagal {len(hasil_gagal)}")
    
    return hasil_sukses, hasil_gagal

if __name__ == "__main__":
    print("\n>>> MEMULAI PROSES PIPELINE <<<")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(base_dir)
    raw_dir = os.path.join(project_dir, 'Data', 'Raw')
    os.makedirs(raw_dir, exist_ok=True)
    json_path = os.path.join(raw_dir, 'tickers_us.json')
    
    with open(json_path, 'r') as file:
            data_json = json.load(file)        
    daftar_saham_tes = [item['yf_symbol'] for item in data_json['tickers']]
    print(f"Berhasil load {len(daftar_saham_tes)} ticker dari JSON!")
    
    start_time = time.time()
    sukses, gagal = uji_tarik_data_saham(
        daftar_ticker=daftar_saham_tes, 
        ui_periode="1 Tahun Terakhir", 
        ui_frekuensi="Harian Daily"
    )
    
    print(f"Waktu Eksekusi {time.time() - start_time:.2f} detik\n")
    
    print(">>> INSPEKSI DATA PARQUET <<<")
    ticker_cek = input("")
    
    if ticker_cek in sukses:
        file_path = os.path.join(raw_dir, f"{ticker_cek}.parquet")
        df_inspeksi = pd.read_parquet(file_path)
        
        print(f"Data {ticker_cek} berhasil diload dari: {file_path}")
        print(f"Total baris: {len(df_inspeksi)}")
        print(f"\nPreview 5 data teratas {ticker_cek}:")
        print(df_inspeksi.head())
        print("\nCek Missing Values (NaN):")
        print(df_inspeksi.isna().sum())
    else:
        print(f"Tidak bisa inspeksi, saham {ticker_cek} gagal ditarik.")