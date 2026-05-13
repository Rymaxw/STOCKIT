import streamlit as st

# Konfigurasi Halaman Dasar (WAJIB dipanggil pertama)
st.set_page_config(
    page_title="STOCKIT - Prediksi Saham AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estetika CSS Kustom (Dark Mode / Premium Look)
st.markdown("""
    <style>
        .main-title {
            font-size: 3.5rem !important;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
        }
        .subtitle {
            font-size: 1.2rem;
            color: #A0AEC0;
            margin-bottom: 2rem;
            margin-top: -10px;
        }
        .card {
            background-color: #1E293B;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            border: 1px solid #334155;
            height: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# Bagian Header Utama
st.markdown('<p class="main-title">STOCKIT: AI Stock Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Platform Keputusan Investasi berbasis Machine Learning (PyCaret) untuk Top 30 US Stocks.</p>', unsafe_allow_html=True)

# Membagi layout menjadi 2 kolom untuk penjelasan fitur
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3 style="color: #94A3B8;">🚀 Fitur Utama</h3>
        <ul style="color: #E2E8F0; line-height: 1.8;">
            <li><b>Prediksi AI (Time-Series):</b> Proyeksi pergerakan saham untuk jangka Mingguan, Bulanan, dan Tahunan secara akurat berdasarkan data historis 15 tahun.</li>
            <li><b>Komparasi Pintar:</b> Bingung pilih AAPL atau GOOGL? Bandingkan dua emiten secara langsung (head-to-head) untuk melihat prospek return terbaik.</li>
            <li><b>Asisten Budget:</b> Masukkan modal investasimu, dan AI akan merekomendasikan alokasi emiten terbaik.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3 style="color: #94A3B8;">🤖 Dapur Pacu (Engine)</h3>
        <p style="color: #E2E8F0; line-height: 1.6;">
        Aplikasi ini ditenagai oleh algoritma Machine Learning canggih yang memilih sendiri permodelan paling cocok untuk setiap emiten.
        <br><br>
        Algoritma yang berlaga di belakang layar termasuk <b>ARIMA, Light Gradient Boosting (LightGBM), Extra Trees, ETS, hingga Theta Forecaster</b>, yang diseleksi ketat berdasarkan metrik <i>Mean Absolute Error (MAE)</i>.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: #334155;'>", unsafe_allow_html=True)
st.info("👈 **Mulai Eksplorasi:** Silakan navigasi melalui menu di *Sidebar* sebelah kiri untuk mengakses fitur-fitur prediksi.")
