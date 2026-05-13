# Penjelasan Parameter Konfigurasi (Dataset Bulanan)

Dalam mengembangkan model *Machine Learning* untuk prediksi saham, penentuan angka-angka konfigurasi tidak dilakukan secara acak, melainkan berdasarkan ilmu ukur Data Science dan pola ekonomi riil. 

Berikut adalah rasionalisasi (alasan) mengapa kita menggunakan `ukuran_training=180`, `horizon_prediksi=12`, dan `jumlah_fold=5` pada data frekuensi bulanan:

---

## 1. Mengapa `ukuran_training` = 180?
`180` pada data bulanan berarti **180 bulan (atau tepatnya 15 Tahun)** masa lalu.

**Alasan Ekonomi & Pasar Saham:**
Siklus ekonomi besar (seperti fase resesi, pemulihan, dan puncak ekonomi/ *Bull Market & Bear Market*) biasanya berputar dalam kurun waktu 5 hingga 10 tahun.
- Jika kita menggunakan data yang terlalu pendek (misal 3 tahun), model AI kita mungkin hanya belajar fase saat saham sedang naik saja, dan akan "kaget" atau gagal memprediksi ketika terjadi krisis.
- Jika kita menggunakan data terlalu panjang (misal 30-40 tahun), dinamika pasar zaman dahulu (tahun 1980-an) sudah tidak relevan dengan pasar modern yang didominasi oleh algoritma trading dan teknologi.
- **Kesimpulan:** 15 tahun (180 bulan) adalah "Sweet Spot" (titik paling ideal) karena model akan sempat mempelajari minimal 1 atau 2 siklus krisis (seperti efek awal pemulihan 2008, perang dagang 2018, dan pandemi 2020), sehingga model lebih tangguh (*robust*).

---

## 2. Mengapa `horizon_prediksi` = 12?
`12` pada data bulanan berarti **12 bulan ke depan (1 Tahun)**.

**Alasan Fungsional Aplikasi:**
- Tujuan utama aplikasi Streamlit ini adalah memberi rekomendasi kepada publik (*user*) untuk **berinvestasi**.
- Prediksi investasi jangka pendek (< 3 bulan) sangat dipengaruhi oleh sentimen berita sesaat atau bandar (*noise* yang tinggi), yang secara teori matematis hampir mustahil ditebak arahnya secara pasti.
- Sebaliknya, memprediksi terlalu jauh (misal 5 tahun ke depan) secara akurat juga sangat sulit karena ketidakpastian dunia.
- **Kesimpulan:** Horizon 1 tahun (12 bulan) adalah standar emas dalam berinvestasi saham yang digunakan oleh manajer investasi profesional untuk menentukan target harga (*Price Target*).

---

## 3. Mengapa `jumlah_fold` = 5?
Di dunia Machine Learning, model tidak boleh langsung dipercaya hanya karena ia menebak 1 kali dengan benar. Kita menggunakan teknik yang dinamakan **Time Series Cross-Validation**.

`jumlah_fold=5` berarti PyCaret akan melakukan **5 kali uji coba (ujian)** secara bergeser ke masa lalu sebelum menyatakan model tersebut akurat.

**Ilustrasi Ujian (Folds):**
- **Fold 1:** Model belajar dari tahun 2009-2023, lalu menebak tahun 2024. Dihitung nilai kesalahannya (Error/MAE).
- **Fold 2:** Mundur selangkah. Model belajar dari 2008-2022, lalu menebak tahun 2023. Dihitung nilai kesalahannya.
- **Fold 3:** Mundur lagi. Belajar 2007-2021, tebak 2022.
- **Fold 4:** Belajar 2006-2020, tebak 2021.
- **Fold 5:** Belajar 2005-2019, tebak 2020.

**Kesimpulan:**
Hasil akhir akurasi model yang kita dapatkan (seperti MAE 0.066) bukanlah hasil tebakan beruntung, melainkan **rata-rata dari 5 ujian berbeda** di 5 tahun yang berbeda. Angka 5 adalah standar industri (*Rule of Thumb*) untuk menyeimbangkan antara tingkat kepercayaan keakuratan model dengan waktu pemrosesan (*computing time*).
