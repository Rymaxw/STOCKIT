import pandas as pd
import numpy as np
import os
import glob


class PengelolaDataSaham:

    def __init__(self, folder_data: str = None):
        if folder_data is None:
            folder_utama = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            folder_data = os.path.join(folder_utama, 'Data', 'Processed')
        self.folder_data = folder_data

    def muat_semua_data(self) -> pd.DataFrame:
        daftar_berkas = glob.glob(os.path.join(self.folder_data, "*_harian_clean.parquet"))
        daftar_df = []

        for berkas in daftar_berkas:
            nama_berkas = os.path.basename(berkas)
            kode_saham = nama_berkas.split('_harian_clean.parquet')[0]

            try:
                df = pd.read_parquet(berkas)
                df['Kode_Saham'] = kode_saham
                daftar_df.append(df)
            except Exception as galat:
                print(f"Gagal memuat {nama_berkas}: {galat}")

        if not daftar_df:
            return pd.DataFrame()

        return pd.concat(daftar_df)


class PenilaiSaham:

    def __init__(self, bobot_return: float = 0.40, bobot_sharpe: float = 0.40, bobot_volatilitas: float = 0.20):
        self.bobot_return = bobot_return
        self.bobot_sharpe = bobot_sharpe
        self.bobot_volatilitas = bobot_volatilitas

    def _hitung_metrik_saham(self, grup: pd.DataFrame) -> dict:
        grup['Profit_Harian'] = grup['Close'].pct_change()
        jumlah_lookback = min(30, len(grup) - 1)
        harga_sekarang = grup['Close'].iloc[-1]
        harga_lalu = grup['Close'].iloc[-(jumlah_lookback + 1)]
        profit_30h = (harga_sekarang - harga_lalu) / harga_lalu

        rata_rata_profit = grup['Profit_Harian'].mean()
        std_profit = grup['Profit_Harian'].std()

        if pd.isna(std_profit) or std_profit == 0:
            rasio_sharpe = 0
            volatilitas = 0
        else:
            rasio_sharpe = (rata_rata_profit / std_profit) * np.sqrt(252)
            volatilitas = std_profit * np.sqrt(252)

        return {
            'Profit_30H': profit_30h,
            'Rasio_Sharpe': rasio_sharpe,
            'Volatilitas': volatilitas,
        }

    def _normalisasi_kolom(self, tabel: pd.DataFrame, kolom: str, dibalik: bool = False) -> pd.Series:
        nilai_min = tabel[kolom].min()
        nilai_max = tabel[kolom].max()
        if nilai_max == nilai_min:
            return pd.Series([0.5] * len(tabel), index=tabel.index)
        hasil = (tabel[kolom] - nilai_min) / (nilai_max - nilai_min)
        return 1 - hasil if dibalik else hasil

    def evaluasi_saham(self, data_saham) -> pd.DataFrame:
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

            metrik = self._hitung_metrik_saham(grup)
            daftar_hasil.append({'Kode_Saham': kode_saham, **metrik})

        tabel_hasil = pd.DataFrame(daftar_hasil)

        if tabel_hasil.empty:
            return tabel_hasil

        tabel_hasil['Profit_30H_Norm']    = self._normalisasi_kolom(tabel_hasil, 'Profit_30H')
        tabel_hasil['Rasio_Sharpe_Norm']  = self._normalisasi_kolom(tabel_hasil, 'Rasio_Sharpe')
        tabel_hasil['Volatilitas_Norm']   = self._normalisasi_kolom(tabel_hasil, 'Volatilitas', dibalik=True)

        tabel_hasil['Skor_Akhir'] = (
            tabel_hasil['Profit_30H_Norm']   * self.bobot_return +
            tabel_hasil['Rasio_Sharpe_Norm'] * self.bobot_sharpe +
            tabel_hasil['Volatilitas_Norm']  * self.bobot_volatilitas
        )

        tabel_hasil = tabel_hasil.sort_values(by='Skor_Akhir', ascending=False).reset_index(drop=True)
        return tabel_hasil.head(5)


if __name__ == "__main__":
    print("Memuat data saham untuk evaluasi")
    folder_utama = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folder_diproses = os.path.join(folder_utama, 'Data', 'Processed')

    pengelola = PengelolaDataSaham(folder_data=folder_diproses)
    data_gabungan = pengelola.muat_semua_data()

    if not data_gabungan.empty:
        print("Melakukan evaluasi saham...")
        penilai = PenilaiSaham()
        saham_terbaik = penilai.evaluasi_saham(data_gabungan)

        print("\n=== TOP 5 SAHAM TERBAIK ===")
        print(saham_terbaik[['Kode_Saham', 'Profit_30H', 'Rasio_Sharpe', 'Volatilitas', 'Skor_Akhir']])
    else:
        print(f"Tidak ada data saham yang dimuat dari {folder_diproses}.")
