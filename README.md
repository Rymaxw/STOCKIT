# STOCKIT — Stock Portfolio Intelligence Toolkit

> Platform analisis data sains berbasis **Streamlit** untuk mengoptimalkan keuntungan portofolio saham AS, dilengkapi prediksi harga berbasis **AI/Machine Learning** menggunakan **PyCaret**.

**PASD'26** — Proyek Sains Data 2026

---

## Ringkasan Fitur

| Fitur | Deskripsi |
|---|---|
| **Eksplorasi Data** | Grafik Candlestick interaktif dengan indikator teknikal lengkap (MA, RSI, MACD, Bollinger Bands, ATR, Volatilitas) |
| **Top Stocks** | Peringkat saham terbaik secara real-time berdasarkan Composite Score (Return 30H, Sharpe Ratio, Volatilitas) |
| **Prediksi Investasi** | Proyeksi harga 1 Minggu, 1 Bulan, dan 1 Tahun ke depan menggunakan model AI PyCaret |
| **Optimasi Portofolio** | Alokasi investasi optimal berbasis Modern Portfolio Theory (MPT) — Markowitz |
| **Pipeline ETL** | Pengunduhan & pemrosesan data saham otomatis dari Yahoo Finance dengan indikator teknikal |
| **Auto-Training** | Pelatihan model time-series otomatis untuk 30 saham × 3 frekuensi (Mingguan, Bulanan, Tahunan) |

---

## Arsitektur Sistem

```
STOCKIT/
├── UI/                          # Antarmuka Web (Streamlit)
│   ├── home.py                  # Halaman Beranda (entry point)
│   ├── pages/
│   │   ├── data_exploration.py  # Eksplorasi data & grafik Candlestick
│   │   ├── top_stocks.py        # Peringkat saham terbaik
│   │   ├── prediction.py        # Prediksi investasi AI
│   │   ├── optimization.py      # Optimasi portofolio Markowitz
│   │   └── about.py             # Halaman tentang aplikasi
│   └── utils/
│       ├── sidebar.py           # Komponen sidebar navigasi
│       ├── data_handler.py      # Handler data untuk UI
│       ├── prediction_engine.py # Engine prediksi (AI + Statistik)
│       └── portfolio_model.py   # Model optimasi portofolio
│
├── Utils/                       # Modul Backend & Engine
│   ├── data_pipeline.py         # Pipeline ETL (fetch, proses, simpan)
│   ├── indikator.py             # Penghitung indikator teknikal
│   ├── scoring.py               # Mesin penilaian & peringkat saham
│   ├── candlestick.py           # Pembuat grafik Candlestick Plotly
│   ├── pelatih_model.py         # Pelatihan model AI (PyCaret)
│   ├── buat_ringkasan_model.py  # Generator ringkasan metadata model
│   ├── st_dataloader.py         # Data loader untuk sesi Streamlit
│   └── sidebar_filter.py        # Filter sidebar lanjutan
│
├── Data/
│   ├── Raw/                     # Data OHLCV mentah (.parquet) + tickers_us.json
│   └── Processed/               # Data teragregasi (mingguan, bulanan, tahunan)
│
├── Models/                      # Model AI terlatih (.pkl) & metadata (.json)
│   ├── Mingguan/
│   ├── Bulanan/
│   └── Tahunan/
│
├── Notebooks/                   # Jupyter Notebooks (EDA, Modeling, Candlestick)
│   ├── 02_eda.ipynb
│   ├── 03_modeling.ipynb
│   ├── candlestick.ipynb
│   └── data_cleaning.ipynb
│
├── fetch_tickers_us.py          # Script validasi & registrasi 30 ticker US
├── requirements.txt             # Dependensi Python
└── .gitignore
```

---

## Prasyarat

- **Python** 3.9 – 3.11 (direkomendasikan 3.10)
- **pip** terbaru
- Koneksi internet (untuk mengunduh data Yahoo Finance)

---

## Instalasi & Setup

### 1. Clone Repository

```bash
git clone https://github.com/Rymaxw/STOCKIT.git
cd STOCKIT
```

### 2. Buat Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

> **Catatan:** Instalasi `pycaret` memerlukan waktu cukup lama karena dependensinya yang banyak (scikit-learn, lightgbm, dll).

---

## Alur Penggunaan (End-to-End Workflow)

Berikut adalah alur lengkap dari awal setup hingga menggunakan seluruh fitur aplikasi:

### Tahap 1 — Validasi Ticker Saham

Jalankan script ini untuk memvalidasi 30 ticker saham US teratas dan menyimpan hasilnya ke `Data/Raw/tickers_us.json`:

```bash
python fetch_tickers_us.py
```

**Output:** `Data/Raw/tickers_us.json` berisi daftar 30 ticker yang telah divalidasi ketersediaan datanya di Yahoo Finance.

### Tahap 2 — Unduh & Proses Data (Pipeline ETL)

Jalankan pipeline untuk mengunduh data OHLCV hingga 21 tahun terakhir, menambahkan indikator teknikal, dan menyimpan hasilnya:

```bash
python -m Utils.data_pipeline
```

**Proses yang dilakukan:**
1. Mengunduh data harian dari Yahoo Finance untuk setiap ticker
2. Menghitung indikator teknikal (MA5, MA20, MA50, RSI-14, MACD, Bollinger Bands, ATR-14, Volatilitas 30H)
3. Menyimpan data mentah + indikator ke `Data/Raw/{TICKER}.parquet`
4. Mengagregasi ke frekuensi mingguan, bulanan, tahunan dan menyimpan ke `Data/Processed/`

### Tahap 3 — Pelatihan Model AI (Opsional, tapi Direkomendasikan)

Latih model prediksi time-series untuk semua saham menggunakan PyCaret:

```bash
python -m Utils.pelatih_model
```

**Proses yang dilakukan:**
1. Memuat data terproses untuk setiap frekuensi (mingguan, bulanan, tahunan)
2. Membuat fitur eksogen (lag indikator teknikal)
3. Melatih dan membandingkan beberapa model ML (Gradient Boosting, Random Forest, Elastic Net, dll.)
4. Menyimpan model terbaik (`.pkl`) dan metadata (`.json`) ke `Models/`
5. Menghasilkan `Models/RINGKASAN_MODEL.md` otomatis

> Proses ini membutuhkan waktu **cukup lama** (tergantung spesifikasi mesin). Terdapat 30 saham × 3 frekuensi = **90 model** yang dilatih.

### Tahap 4 — Jalankan Aplikasi Web

```bash
streamlit run UI/home.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`.

---

## Panduan Halaman Aplikasi

### Home (Beranda)

Halaman utama dengan navigasi cepat ke fitur-fitur utama. Saat pertama kali diakses, sistem otomatis melakukan sinkronisasi data terbaru dari Yahoo Finance (di-cache selama 1 jam).

### Eksplorasi Data

1. Masukkan ticker saham (contoh: `AAPL, MSFT, GOOGL`)
2. Pilih rentang waktu analisis
3. Klik **Load Data**
4. Aktifkan indikator teknikal yang ingin ditampilkan (Bollinger Bands, RSI, MACD, ATR, Volatilitas, MA5)
5. Lihat grafik Candlestick interaktif per saham dan grafik perbandingan antar saham

### Top Stocks

Menampilkan peringkat saham terbaik secara real-time berdasarkan:
- **Composite Score** = 40% Return 30H + 40% Sharpe Ratio + 20% Volatilitas (dibalik)
- Grafik Risk-Return Scatter Plot (Efficient Frontier)
- Grafik Candlestick 60 hari dengan SMA-20 dan Volume

### Prediksi Investasi

1. Masukkan **budget investasi** (dalam Rupiah)
2. Pilih mode: **Rekomendasi Otomatis** atau **Pilih Saham Sendiri**
3. Klik **Analisis Investasi**
4. Lihat kartu proyeksi harga per saham (1 Minggu / 1 Bulan / 1 Tahun)
5. Lihat grafik historis + garis prediksi dan chart perbandingan return

> Model AI PyCaret digunakan jika tersedia. Jika tidak, fallback ke metode statistik (rata-rata log return).

### Optimasi Portofolio

1. Pilih saham yang ingin dioptimasi
2. Pilih metode (Maximize Sharpe Ratio / Minimize Risk)
3. Masukkan modal awal (dalam Rupiah)
4. Klik **Jalankan Optimasi**
5. Lihat metrik ringkasan (Proyeksi Return, Volatilitas, Sharpe Ratio)
6. Lihat alokasi bobot optimal, tab kinerja, Efficient Frontier, dan metadata model AI
7. Lihat tabel Action Plan dengan rekomendasi alokasi modal

---

## Indikator Teknikal yang Tersedia

| Indikator | Deskripsi |
|---|---|
| **MA5 / MA20 / MA50** | Moving Average (Rerata Bergerak) 5, 20, 50 periode |
| **RSI-14** | Relative Strength Index — mengukur momentum harga |
| **MACD** | Moving Average Convergence Divergence (garis, sinyal, histogram) |
| **Bollinger Bands** | Pita volatilitas (atas, tengah, bawah) dengan deviasi standar 2σ |
| **ATR-14** | Average True Range — mengukur volatilitas harian |
| **Volatilitas 30H** | Volatilitas bergulir 30 hari yang dianualisasi |

---

## Daftar 30 Saham yang Dianalisis

| Sektor | Saham |
|---|---|
| **Tech Giants** | AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA |
| **Semiconductors** | AVGO, AMD, ORCL |
| **Financials** | BRK-B, JPM, V, MA, BAC |
| **Healthcare** | LLY, UNH, JNJ, MRK, ABBV |
| **Consumer** | WMT, PG, COST, HD, KO, PEP |
| **Energy & Others** | CVX, XOM, CRM, NFLX |

---

## Tech Stack

| Komponen | Teknologi |
|---|---|
| **Frontend** | Streamlit, Plotly, HTML/CSS (Glassmorphism, Space Grotesk font) |
| **Backend** | Python, Pandas, NumPy |
| **Data Source** | Yahoo Finance (via `yfinance`) |
| **ML/AI** | PyCaret (Time Series Forecasting) |
| **Storage** | Apache Parquet (via `pyarrow`) |
| **Theme** | Dark mode dengan aksen biru langit (#00d1ff, #a4e6ff) |

---

## Format Data

- **Data Mentah:** `Data/Raw/{TICKER}.parquet` — OHLCV harian + indikator teknikal
- **Data Teragregasi:** `Data/Processed/{TICKER}_{frekuensi}.parquet` — mingguan, bulanan, tahunan
- **Ticker Registry:** `Data/Raw/tickers_us.json` — daftar ticker yang tervalidasi
- **Model AI:** `Models/{Frekuensi}/{TICKER}_model_{frekuensi}.pkl` — model PyCaret terlatih
- **Metadata Model:** `Models/{Frekuensi}/{TICKER}_metadata.json` — info model terbaik & metrik

---

## Catatan Penting

- Pastikan koneksi internet aktif saat pertama kali menjalankan aplikasi (data diunduh dari Yahoo Finance).
- File `.parquet` dan `.pkl` (model) tidak disertakan di repository karena ukurannya besar. Jalankan Tahap 1–3 untuk men-generate ulang.
- Aplikasi memerlukan **Python 3.9–3.11**. PyCaret belum sepenuhnya mendukung Python 3.12+.
- Prediksi harga bersifat **proyeksi statistik/model**, bukan saran investasi finansial.

---

## Lisensi

Proyek ini dikembangkan untuk keperluan akademis (Proyek Akhir Sains Data 2026).
