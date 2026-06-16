# 📋 LOG PERUBAHAN & PENYEMPURNAAN APLIKASI (STOCKIT)
*Tanggal Pembaruan: 16 Juni 2026*

Dokumen ini berisi rangkuman log perubahan teknis pada sistem backend, mesin analisis data, dan antarmuka (UI) web Streamlit **STOCKIT**.

---

## 🛠️ 1. Pembaruan Mesin Penilaian & ETL (Backend)

### 📄 Berkas: [scoring.py](file:///Users/ajarsaktiwp/Documents/STOCKIT/Utils/scoring.py)
* **Perubahan**: Menambahkan ekstraksi harga penutupan terakhir (`Harga_Terakhir`) dan persentase perubahan harian (`Perubahan_Harian`) di dalam fungsi `_hitung_metrik_saham`.
* **Fungsi**: Memungkinkan dashboard mengambil data harga teranyar dan mengalkulasi persentase kenaikan/penurunan harga saham harian (hari ini vs kemarin) secara otomatis.
* **Kompatibilitas**: Bersifat *additive* (tambahan kolom), sehingga tidak merusak fungsi penilaian portofolio bawaan pada modul lainnya.

### 📄 Berkas: [data_handler.py](file:///Users/ajarsaktiwp/Documents/STOCKIT/UI/utils/data_handler.py)
* **Perubahan**: 
  * Mengubah output fungsi `ambil_saham_terbaik_live` dari tipe `pd.DataFrame` menjadi tipe data `dict` yang mengemas data tabel terformat (`tabel`), data tren penutupan (`historis`), dan data OHLCV lengkap (`ohlcv`).
  * Memperbarui fungsi `_format_hasil_penilaian` untuk menambahkan format mata uang USD ($) pada harga dan memformat persentase perubahan harian secara dinamis jika datanya tersedia.
* **Fungsi**: Mendukung visualisasi grafik Candlestick interaktif secara real-time langsung dari server Yahoo Finance.

---

## 🖥️ 2. Peningkatan Visualisasi Antarmuka (UI/Frontend)

### 📄 Berkas: [top_stocks.py](file:///Users/ajarsaktiwp/Documents/STOCKIT/UI/pages/top_stocks.py) (Redesain Total)
* **Perubahan**:
  * **Top 5 Podium Cards**: Menampilkan 5 saham teratas dalam tata letak kartu bertema *glassmorphism* modern dengan indikator Rank Badge (Juara 🥇, 🥈, 🥉), harga riil dalam USD, badge persentase perubahan harian (hijau naik, merah turun), Composite Score dalam bar visual gradien, dan level risiko.
  * **Risk-Return Scatter Plot**: Menambahkan grafik sebar Plotly untuk memetakan performa saham berdasarkan *Efficient Frontier* (Sumbu X: Risiko/Volatilitas %, Sumbu Y: Return 30H %). Ukuran gelembung mewakili Composite Score.
  * **Interactive Candlestick Chart**: Menambahkan visualisasi grafik Candlestick 60 hari lengkap dengan garis rata-rata bergerak (SMA 20) dan subplot Volume transaksi yang dapat diubah secara interaktif lewat selektor dropdown.
  * **Penyesuaian Masukan**: Menghapus grafik sparkline area kecil di bawah kartu agar visualisasi dashboard terlihat bersih (*clean*) dan minimalis.

### 📄 Berkas: [prediction.py](file:///Users/ajarsaktiwp/Documents/STOCKIT/UI/pages/prediction.py)
* **Perubahan**:
  * **Grafik Historis & Proyeksi**: Menambahkan grafik garis interaktif per-saham yang memvisualisasikan data harga historis 90 hari terakhir (warna biru langit) dan menyambungkannya dengan garis putus-putus (*dotted line*) ke titik proyeksi target masa depan (simbol diamond, berwarna hijau untuk return positif dan merah untuk return negatif).
  * **Penyederhanaan Layout**: Mengatur visualisasi agar dirender 2 grafik berdampingan per baris untuk kenyamanan navigasi mata pengguna.
  * **Pembersihan Emojis**: Menghapus emoji kalender (`📅`) pada tab proyeksi jangka waktu (1 Minggu, 1 Bulan, 1 Tahun) demi desain yang minimalis dan rapi.

### 📄 Berkas: [sidebar.py](file:///Users/ajarsaktiwp/Documents/STOCKIT/UI/utils/sidebar.py)
* **Perubahan**: Menyuntikkan aturan gaya CSS global `a.header-anchor { display: none !important; }` di dalam style tag sidebar utama.
* **Fungsi**: Menyembunyikan ikon jangkar tautan (`🔗`) bawaan Streamlit secara global yang biasa muncul ketika kursor diarahkan ke judul/heading, sehingga visual aplikasi benar-benar bersih (*clean*).

---

## 🔬 3. Status Validasi & Pengujian

Semua perubahan telah diuji secara internal dan berjalan lancar pada server Streamlit aktif:
1. **Sintaksis & Interpretasi Kode**: Seluruh file berhasil dievaluasi tanpa error.
2. **Kesesuaian Desain**: Tema gelap (*dark theme*) dengan aksen biru langit berpendar konsisten di seluruh elemen visual.
3. **Kompatibilitas Mundur**: Pembuatan perbandingan portofolio investasi di halaman optimasi tidak terganggu dengan perubahan struktur output.
