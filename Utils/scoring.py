import pandas as pd
import numpy as np
import os
import glob

class PengelolaDataSaham:
    def __init__(self, folder_data='data/processed'):
        self.folder_data = folder_data

    def muat_semua_data(self):
        daftar_berkas = glob.glob(os.path.join(self.folder_data, "*_clean.parquet"))
        daftar_df = []
        
        for berkas in daftar_berkas:
            nama_berkas = os.path.basename(berkas)
            kode_saham = nama_berkas.split('_clean.parquet')[0]
            
            try:
                df = pd.read_parquet(berkas)
                df['Kode_Saham'] = kode_saham
                daftar_df.append(df)
            except Exception as e:
                print(f"Gagal memuat {nama_berkas}: {e}")
                
        if not daftar_df:
            return pd.DataFrame()
            
        return pd.concat(daftar_df)

class PenilaiSaham:
    def __init__(self, bobot_return=0.40, bobot_sharpe=0.40, bobot_volatilitas=0.20):
        self.bobot_return = bobot_return
        self.bobot_sharpe = bobot_sharpe
        self.bobot_volatilitas = bobot_volatilitas

    def evaluasi_saham(self, data_saham):
        if isinstance(data_saham, dict):
            daftar_df = []
            for kode_saham, data in data_saham.items():
                temp = data.copy()
                temp['Kode_Saham'] = kode_saham
                daftar_df.append(temp)
            data_saham = pd.concat(daftar_df)
            
        daftar_hasil = []
        
        for kode_saham, grup in data_saham.groupby('Kode_Saham'):
            grup = grup.sort_index()
            
            if len(grup) < 2:
                continue
                
            grup['Profit_Harian'] = grup['Close'].pct_change()
            lookback = min(30, len(grup) - 1)
            harga_sekarang = grup['Close'].iloc[-1]
            harga_lalu = grup['Close'].iloc[-(lookback + 1)]
            profit_30h = (harga_sekarang - harga_lalu) / harga_lalu
            
            rata_rata_profit = grup['Profit_Harian'].mean()
            std_profit = grup['Profit_Harian'].std()
            
            if pd.isna(std_profit) or std_profit == 0:
                rasio_sharpe = 0
                volatilitas = 0
            else:
                rasio_sharpe = (rata_rata_profit / std_profit) * np.sqrt(252)
                volatilitas = std_profit * np.sqrt(252)
                
            daftar_hasil.append({
                'Kode_Saham': kode_saham,
                'Profit_30H': profit_30h,
                'Rasio_Sharpe': rasio_sharpe,
                'Volatilitas': volatilitas
            })
            
        tabel_hasil = pd.DataFrame(daftar_hasil)
        
        if tabel_hasil.empty:
            return tabel_hasil
            
        for kolom in ['Profit_30H', 'Rasio_Sharpe']:
            nilai_min = tabel_hasil[kolom].min()
            nilai_max = tabel_hasil[kolom].max()
            if nilai_max != nilai_min:
                tabel_hasil[kolom + '_Norm'] = (tabel_hasil[kolom] - nilai_min) / (nilai_max - nilai_min)
            else:
                tabel_hasil[kolom + '_Norm'] = 0.5
                
        vol_min = tabel_hasil['Volatilitas'].min()
        vol_max = tabel_hasil['Volatilitas'].max()
        if vol_max != vol_min:
            tabel_hasil['Volatilitas_Norm'] = 1 - ((tabel_hasil['Volatilitas'] - vol_min) / (vol_max - vol_min))
        else:
            tabel_hasil['Volatilitas_Norm'] = 0.5
            
        tabel_hasil['Skor_Akhir'] = (
            tabel_hasil['Profit_30H_Norm'] * self.bobot_return +
            tabel_hasil['Rasio_Sharpe_Norm'] * self.bobot_sharpe +
            tabel_hasil['Volatilitas_Norm'] * self.bobot_volatilitas
        )
        
        tabel_hasil = tabel_hasil.sort_values(by='Skor_Akhir', ascending=False).reset_index(drop=True)

        return tabel_hasil.head(5)

if __name__ == "__main__":
    print("Memuat data saham untuk evaluasi")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, 'Data', 'Processed')
    
    pengelola = PengelolaDataSaham(folder_data=target_dir)
    data_gabungan = pengelola.muat_semua_data()
    
    if not data_gabungan.empty:
        print("Melakukan evaluasi saham")
        penilai = PenilaiSaham()
        saham_terbaik = penilai.evaluasi_saham(data_gabungan)
        
        print("\n=== TOP 5 SAHAM TERBAIK ===")
        print(saham_terbaik[['Kode_Saham', 'Profit_30H', 'Rasio_Sharpe', 'Volatilitas', 'Skor_Akhir']])
    else:
        print(f"Tidak ada data saham yang dimuat dari {target_dir}.")
