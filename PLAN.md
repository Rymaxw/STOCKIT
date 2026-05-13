# Rencana Refactoring & Standardisasi Proyek (PLAN)

## 1. Tujuan
Menyelaraskan struktur kode, penamaan variabel/fungsi, dan penanganan path pada berkas-berkas utility dan *notebooks* agar sesuai dengan standar yang ditetapkan pada `Utils/data_pipeline.py` (Clean Code, OOP, FP, dan Bahasa Indonesia).

## 2. Analisis Berkas & Ketidakkonsistenan

### A. `Utils/scoring.py`
- **Penamaan**: Sebagian besar sudah menggunakan Bahasa Indonesia (contoh: `PengelolaDataSaham`, `PenilaiSaham`, `evaluasi_saham`). Namun, blok utama pemanggilan masih memiliki variabel seperti `base_dir`, `target_dir` yang sebaiknya diubah menjadi `folder_utama`, `folder_target`.
- **Path**: Path default pada konstruktor `__init__` masih menggunakan *hardcoded string* `'data/processed'` (huruf kecil). Berbeda dengan `data_pipeline.py` yang menggunakan struktur kapitalisasi yang benar seperti `os.path.join(folder_proyek, 'Data', 'Processed')`.

### B. `Utils/sidebar_filter.py`
- **Penamaan**: Hampir seluruhnya masih menggunakan Bahasa Inggris (contoh: `render_sidebar_filter`, `apply_filters`, `format_ranking_table`, `TICKERS_DEFAULT`, `PERIOD_MAP`, `SORT_COLUMNS`).
- **Paradigma**: Belum sepenuhnya OOP.
- **Tindakan**: 
  - Mengubah penamaan menjadi Bahasa Indonesia (contoh: `TICKER_BAWAAN`, `PETA_PERIODE`, `KOLOM_URUTAN`, `terapkan_filter`, `format_tabel_peringkat`).
  - Membungkus fungsi menjadi kelas (misal: `FilterSidebar`) jika dirasa perlu untuk menerapkan prinsip OOP secara penuh.

### C. `Utils/candlestick.py`
- **Penamaan**: Seluruhnya menggunakan Bahasa Inggris (contoh: `CandlestickTheme`, `StockDataLoader`, `CandlestickChart`, `ComparisonChart`).
- **Path**: Path pada `_load_from_parquet` sedikit berbeda implementasinya dan menggunakan variabel bahasa Inggris.
- **Tindakan**:
  - Mengubah nama kelas menjadi Bahasa Indonesia (`TemaCandlestick`, `PemuatDataSaham`, `GrafikCandlestick`, `GrafikKomparasi`).
  - Mengubah atribut, method, dan variabel pendukung menjadi Bahasa Indonesia (contoh: `load_stock_data` -> `muat_data_saham`, `plot_candlestick` -> `buat_grafik_candlestick`).
  - Memastikan *pathing* merujuk pada standar `os.path.abspath(__file__)` seperti pada `data_pipeline.py`.

### D. Notebooks (`Notebooks/02_eda.ipynb`, `Notebooks/data_cleaning.ipynb`)
- Jika modul-modul dari `Utils/` (terutama `candlestick.py` dan `scoring.py`) diimpor ke dalam *notebooks*, penyesuaian nama fungsi/kelas yang dipanggil juga harus dilakukan secara serempak di dalam *notebooks* untuk mencegah error.
- Memastikan path pembacaan data di *notebook* selaras dengan letak direktori `Data/Processed` yang dikonfigurasi di *pipeline*.

## 3. Langkah Eksekusi (Action Items)

1. **Tahap 1: Refaktor `Utils/scoring.py`**
   - Perbaiki default parameter `folder_data` menggunakan deteksi jalur *absolute* berbasis `__file__`.
   - Terjemahkan sisa variabel (*base_dir*, dll.) ke Bahasa Indonesia.

2. **Tahap 2: Refaktor `Utils/sidebar_filter.py`**
   - Terjemahkan konstanta (`TICKER_BAWAAN`, `PETA_PERIODE`, dsb).
   - Terjemahkan nama fungsi ke bahasa Indonesia dan terapkan arsitektur class/OOP.

3. **Tahap 3: Refaktor `Utils/candlestick.py`**
   - Ubah nama-nama *Class* utama dan variabel internal ke Bahasa Indonesia.
   - Ubah *wrapper functions* agar namanya selaras, namun tetap mempertahankan fungsionalitas yang ada (mengingat grafik menggunakan *Plotly*).

4. **Tahap 4: Update Impor (Notebooks & Aplikasi Utama)**
   - Lakukan pencarian dan penggantian impor (contoh: dari `plot_candlestick` menjadi `buat_grafik_candlestick`) pada `app.py`, UI/Pages, dan seluruh Notebooks agar tidak ada _dependency_ yang terputus pasca-refaktoring.

## 4. Referensi Standar (`Utils/data_pipeline.py`)
- Penamaan Kelas: *PascalCase* Berbahasa Indonesia (contoh: `PembersihanData`).
- Penamaan Fungsi/Variabel: *snake_case* Berbahasa Indonesia (contoh: `bersihkan_data`).
- Pengelolaan Path: Menggunakan `os.path.join(folder_proyek, 'Folder', 'Subfolder')`.
