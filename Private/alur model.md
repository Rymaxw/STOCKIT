# Penjelasan Alur Model PyCaret Berdasarkan Frekuensi Waktu

Sesuai dengan prinsip *Clean Code* (menghindari banyak percabangan `if/else` yang membingungkan), skrip `Utils/pelatih_model.py` menggunakan pendekatan **Data Dictionary** dan **Dataclass** untuk memisahkan logika (algoritma) dari konfigurasi. 

Berikut adalah penjelasan detail bagian mana yang mengatur alur Mingguan, Bulanan, dan Tahunan.

---

## 1. Jantung Pengaturan: `DAFTAR_KONFIGURASI`
Coba lihat mulai dari Baris ke-27 di `Utils/pelatih_model.py`. Ada sebuah *dictionary* bernama `DAFTAR_KONFIGURASI`. Ini adalah pusat kendalinya.

```python
DAFTAR_KONFIGURASI = {
    'mingguan': KonfigurasiWaktu(...),
    'bulanan': KonfigurasiWaktu(...),
    'tahunan': KonfigurasiWaktu(...)
}
```

Setiap frekuensi waktu dikemas ke dalam objek `KonfigurasiWaktu`. Mari kita bedah perbedaannya:

### 🔵 Konfigurasi Mingguan (`mingguan`)
```python
    'mingguan': KonfigurasiWaktu(
        nama='mingguan',
        sufiks_berkas='_mingguan.parquet', # File yang akan dimuat
        frekuensi_pandas='W',              # Format waktu Pandas (Weekly)
        horizon_prediksi=4,                # Memprediksi 4 minggu ke depan (~1 bulan)
        periode_musiman=52,                # Siklus musiman 1 tahun ada 52 minggu
        ukuran_training=780,               # Menggunakan 780 minggu (15 tahun) masa lalu
        jumlah_fold=3,                     # Dibagi 3 lipatan saat validasi (cross-validation)
    )
```

### 🟢 Konfigurasi Bulanan (`bulanan`)
```python
    'bulanan': KonfigurasiWaktu(
        nama='bulanan',
        sufiks_berkas='_bulanan.parquet', 
        frekuensi_pandas='M',             
        horizon_prediksi=12,               # Memprediksi 12 bulan ke depan (1 tahun)
        periode_musiman=12,                # Siklus musiman 1 tahun ada 12 bulan
        ukuran_training=180,               # Menggunakan 180 bulan (15 tahun) masa lalu
        jumlah_fold=5,                     
    )
```

### 🔴 Konfigurasi Tahunan (`tahunan`)
```python
    'tahunan': KonfigurasiWaktu(
        nama='tahunan',
        sufiks_berkas='_tahunan.parquet', 
        frekuensi_pandas='Y',             
        horizon_prediksi=1,                # Memprediksi 1 tahun ke depan
        periode_musiman=1,                 # Tidak ada siklus musiman tahunan (1)
        ukuran_training=15,                # Menggunakan 15 tahun masa lalu
        jumlah_fold=2,                     # Fold lebih sedikit karena datanya pendek (hanya 15 baris)
    )
```

---

## 2. Bagaimana Skrip Menjalankannya?

Ketika kita menjalankan fungsi `latih_semua_saham` di bagian bawah (*main execution*), kita memasukkan parameter string frekuensinya:

```python
orkestrator.latih_semua_saham(daftar_saham, frekuensi='tahunan')
```

**Alurnya berlanjut seperti ini:**

1. **Pemilihan Konfigurasi:** Skrip akan mengambil isi dari `DAFTAR_KONFIGURASI['tahunan']`.
2. **Pemuatan Data (`PemuatDataModel`):** Skrip akan otomatis memanggil `sufiks_berkas` (misal: `AAPL_tahunan.parquet`).
3. **Pemotongan Data (`potong_data`):** Skrip akan mengambil data 15 baris (sesuai `ukuran_training=15`) dari bagian terbawah (terbaru).
4. **Validasi Toleransi Minimum:** Skrip mengecek apakah datanya cukup. (Minimal harus punya 3 kali lipat dari `horizon_prediksi`).
5. **Injeksi ke PyCaret (`PelatihModelPyCaret`):** Variabel seperti `horizon_prediksi` dan `periode_musiman` langsung dimasukkan ke argumen `setup()` milik PyCaret.
   ```python
   setup(
       data=data[['Log_Return']],
       fh=konfigurasi.horizon_prediksi, # Masuk ke sini
       fold=konfigurasi.jumlah_fold,    # Masuk ke sini
       seasonal_period=param_musiman,   # Masuk ke sini
       ...
   )
   ```
6. **Penyimpanan Dinamis (`_siapkan_folder_model`):** PyCaret otomatis menyimpan hasil modelnya ke dalam folder yang namanya sesuai dengan konfigurasi (misal: `Models/Tahunan/AAPL_model_tahunan.pkl`).

Dengan teknik *Dataclass Injection* seperti ini, jika suatu saat kamu ingin menambah fitur prediksi **Harian**, kamu **TIDAK PERLU** merombak ratusan baris kode. Kamu cukup menambahkan satu *dictionary* `'harian'` di bagian `DAFTAR_KONFIGURASI` saja!
