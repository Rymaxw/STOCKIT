# Plan: Pengembangan UI/UX Streamlit (Fase 3)

## Tujuan
Membuat antarmuka web (UI) interaktif, modern, dan mudah dipahami oleh kalangan umum (*General Public*) untuk menampilkan hasil prediksi saham, perbandingan, dan rekomendasi berbasis *budget*.

## Struktur Navigasi (Multi-page Streamlit)
Aplikasi akan menggunakan struktur multi-halaman bawaan Streamlit:
1. `app.py`: File utama (*entry point*) untuk konfigurasi halaman global (tema, *page title*, dll).
2. `Pages/1_📊_Prediksi_Saham.py`: Menampilkan prediksi masa depan (Mingguan, Bulanan, Tahunan) dari model yang sudah dilatih, lengkap dengan *chart* interaktif (candlestick & line chart).
3. `Pages/2_⚖️_Komparasi.py`: Menampilkan perbandingan 2 saham (misal: AAPL vs GOOGL). Menunjukkan metrik perbandingan dan pemenangnya berdasarkan proyeksi return.
4. `Pages/3_💰_Rekomendasi_Budget.py`: *Wizard* interaktif tempat pengguna memasukkan modal (contoh: $1000) dan target waktu (1 Bulan). Aplikasi akan memberikan rekomendasi alokasi saham terbaik.

## Komponen UI / Estetika
Aplikasi harus memukau (*wow factor*):
- **Dashboard Metric**: Menggunakan `st.metric` dengan panah hijau/merah (*delta*).
- **Interactive Charts**: Menggunakan `plotly` untuk *candlestick* interaktif, agar pengguna bisa melihat detail saat *hover*.
- **Warna & Tema**: Menggunakan tema gelap (Dark Mode) khas *dashboard crypto/trading* yang premium, dipadukan dengan aksen warna cerah (hijau neon/biru muda).
- **Layout Modular**: Menggunakan `st.columns` dan `st.tabs` agar informasi tidak bertumpuk di satu layar.

## Langkah Eksekusi (Action Items)
1. Inisialisasi struktur file dan folder (`Pages/`).
2. Tulis `app.py` sebagai kerangka utama.
3. Kembangkan halaman `1_📊_Prediksi_Saham.py` terlebih dahulu karena ini adalah fitur paling fundamental yang menghubungkan `.pkl` dan `_metadata.json`.
4. Berikan *mockup* data jika diperlukan, lalu sambungkan dengan model *real*.
