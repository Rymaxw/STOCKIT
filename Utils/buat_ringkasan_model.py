import os
import json
import glob
import pandas as pd
from pathlib import Path

class PengekstrakMetadata:
    def __init__(self):
        self.folder_proyek = Path(__file__).resolve().parent.parent
        self.folder_models = self.folder_proyek / 'Models'
        self.frekuensi_list = ['Mingguan', 'Bulanan', 'Tahunan']

    def ambil_ringkasan(self) -> pd.DataFrame:
        data_ringkasan = []
        
        for frekuensi in self.frekuensi_list:
            folder_frekuensi = self.folder_models / frekuensi
            if not folder_frekuensi.exists():
                continue
                
            file_metadatas = sorted(glob.glob(str(folder_frekuensi / "*_metadata.json")))
            
            for file_path in file_metadatas:
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        
                    kode = data.get('kode_saham', 'N/A')  
                    jumlah_data = data.get('jumlah_data_training', 0)
                    
                    try:
                        top1_key = list(data['metrik_top5']['Model'].keys())[0]
                        
                        model_name = data['metrik_top5']['Model'].get(top1_key, data.get('model_terbaik', 'N/A'))
                        
                        mae_dict = data['metrik_top5'].get('MAE', {})
                        r2_dict = data['metrik_top5'].get('R2', {})
                        
                        mae = mae_dict.get(top1_key)
                        r2 = r2_dict.get(top1_key)
                        
                        if mae is not None: mae = float(mae)
                        if r2 is not None: r2 = float(r2)
                    except Exception:
                        model_name = data.get('model_terbaik', 'N/A')
                        mae = None
                        r2 = None
                        
                    catatan_r2 = ''
                    if r2 is None:
                        if frekuensi == 'Tahunan':
                            catatan_r2 = f'Data terlalu sedikit ({jumlah_data} baris) untuk hitung R2'
                        else:
                            catatan_r2 = 'R2 tidak tersedia dari PyCaret'
                        
                    data_ringkasan.append({
                        'Frekuensi': frekuensi,
                        'Kode_Saham': kode,
                        'Model_Pemenang': model_name,
                        'MAE': mae,
                        'R_Squared': r2
                    })
                except Exception as e:
                    print(f"Gagal membaca {file_path}: {e}")
        df = pd.DataFrame(data_ringkasan)
        if not df.empty:
            df = df.sort_values(by=['Frekuensi', 'Kode_Saham']).reset_index(drop=True)
            
        return df

if __name__ == "__main__":
    ekstraktor = PengekstrakMetadata()
    df_ringkasan = ekstraktor.ambil_ringkasan()
    
    pd.set_option('display.max_rows', 100)
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 1000)
    
    print("\n" + "="*80)
    print(" TABEL RINGKASAN MODEL AI TERBAIK (KESELURUHAN) ")
    print("="*80)
    print(df_ringkasan)
    print("="*80 + "\n")