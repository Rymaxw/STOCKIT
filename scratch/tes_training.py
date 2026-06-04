import os
import sys
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.pelatih_model import OrkestratorPelatihan, DAFTAR_KONFIGURASI

def main():
    print("=== PENGUJIAN PELATIHAN MODEL DENGAN FITUR EKSOGEN ===")
    
    folder_proyek = Path(__file__).resolve().parent.parent
    orkestrator = OrkestratorPelatihan(folder_proyek)
    
    # Gunakan saham GOOGL untuk pengujian model 'tahunan' (data sedikit, proses cepat)
    ticker = "GOOGL"
    konfigurasi = DAFTAR_KONFIGURASI['tahunan']
    
    print(f"Melatih model '{konfigurasi.nama}' untuk saham {ticker}...")
    
    kode, sukses, pesan = orkestrator.latih_satu_saham(ticker, konfigurasi)
    print(f"Hasil: {kode} | Sukses: {sukses} | Pesan: {pesan}")
    
    # Uji model mingguan (opsional tapi bagus untuk pembuktian)
    konfigurasi_mingguan = DAFTAR_KONFIGURASI['mingguan']
    print(f"\nMelatih model '{konfigurasi_mingguan.nama}' untuk saham {ticker} (hanya training)...")
    try:
        df = orkestrator.pemuat.muat_dan_siapkan(ticker, konfigurasi_mingguan)
        df_potong = orkestrator.pemuat.potong_data(df, konfigurasi_mingguan)
        print(f"Bentuk data training mingguan: {df_potong.shape}")
        print(f"Kolom yang diumpankan ke model: {[c for c in df_potong.columns if c == 'Log_Return' or '_Lag' in c]}")
        
        # Jalankan setup saja tanpa training penuh untuk menguji keabsahan setup PyCaret
        from pycaret.time_series import setup
        param_musiman = konfigurasi_mingguan.periode_musiman if konfigurasi_mingguan.periode_musiman > 1 else 1
        kolom_fitur = [c for c in df_potong.columns if c == 'Log_Return' or '_Lag' in c]
        
        s = setup(
            data=df_potong[kolom_fitur],
            target='Log_Return',
            fh=konfigurasi_mingguan.horizon_prediksi,
            fold=konfigurasi_mingguan.jumlah_fold,
            fold_strategy='sliding',
            seasonal_period=param_musiman,
            session_id=123,
            verbose=False,
        )
        print("Setup PyCaret berhasil tanpa error!")
    except Exception as e:
        print(f"Error saat menguji setup mingguan: {e}")
        
    print("\n=== PENGUJIAN SELESAI ===")

if __name__ == "__main__":
    main()
