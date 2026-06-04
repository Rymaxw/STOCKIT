import warnings
warnings.filterwarnings("ignore")

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import datetime
from utils.sidebar import dapatkan_html_sidebar
from Utils.candlestick import (
    PemuatDataSaham, GrafikCandlestick, GrafikKomparasi, TemaCandlestick, buat_grafik_candlestick
)


class HalamanEksplorasiData:

    def __init__(self):
        st.set_page_config(
            page_title="Data Exploration",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    def _suntik_gaya(self):
        st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>', unsafe_allow_html=True)
        st.markdown('<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet"/>', unsafe_allow_html=True)
        
        # Ambient Orbs Background & Main App background
        st.markdown("""<style>.stApp{background-color:#0b0c10;color:#e2e1f0;font-family:'Inter',sans-serif;}.stApp::before{content:'';position:fixed;top:-20%;left:-10%;width:70vw;height:70vw;background:radial-gradient(circle, rgba(0, 209, 255, 0.08) 0%, rgba(0, 209, 255, 0) 70%);border-radius:50%;z-index:-1;pointer-events:none;}.stApp::after{content:'';position:fixed;bottom:-30%;right:-20%;width:80vw;height:80vw;background:radial-gradient(circle, rgba(49, 49, 192, 0.05) 0%, rgba(49, 49, 192, 0) 70%);border-radius:50%;z-index:-1;pointer-events:none;}[data-testid="stHeader"]{display:none!important}.block-container{padding-top:2rem!important; padding-bottom:2rem!important;}</style>""", unsafe_allow_html=True)
        
        # Glass Inputs
        st.markdown("""<style>
        .stTextInput input, .stDateInput input, .stSelectbox [data-baseweb="select"] {
            background: rgba(0,0,0,0.2) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: #e2e1f0 !important;
            border-radius: 0.5rem !important;
            font-family: 'Inter', sans-serif !important;
            padding: 12px !important;
            transition: all 0.3s ease !important;
            min-height: 48px !important;
        }
        .stSelectbox [data-baseweb="select"] {
            padding: 0 12px !important;
        }
        .stTextInput input:focus, .stDateInput input:focus {
            border-color: rgba(0,209,255,0.5) !important;
            box-shadow: 0 0 15px rgba(0,209,255,0.1) !important;
            background: rgba(0,0,0,0.3) !important;
        }
        </style>""", unsafe_allow_html=True)
        
        # Labels
        st.markdown("""<style>[data-testid="stWidgetLabel"]{font-family:'Inter',sans-serif!important;color:#bbc9cf!important;font-size:11px!important}[data-testid="stWidgetLabel"] p{font-size:11px!important}</style>""", unsafe_allow_html=True)
        
        # Glass Buttons
        st.markdown("""<style>[data-testid="stButton"] button{background:linear-gradient(135deg, rgba(0,209,255,0.1), rgba(0,103,127,0.2))!important;border:1px solid rgba(0,209,255,0.3)!important;color:#00d1ff!important;border-radius:0.5rem!important;font-family:'Inter',sans-serif!important;font-weight:500!important;padding:12px 24px!important;height:auto!important;transition:all 0.3s ease!important;backdrop-filter:blur(8px)!important;margin-top:28px!important}[data-testid="stButton"] button:hover{background:linear-gradient(135deg, rgba(0,209,255,0.2), rgba(0,103,127,0.3))!important;border-color:rgba(0,209,255,0.6)!important;box-shadow:0 0 20px rgba(0,209,255,0.2)!important;transform:translateY(-1px)!important}</style>""", unsafe_allow_html=True)
        
        # Checkbox styling
        st.markdown("""<style>.stCheckbox label span{color:#bbc9cf!important;font-family:'Space Grotesk',sans-serif!important;font-size:13px!important}</style>""", unsafe_allow_html=True)

        # Scrollbars
        st.markdown("""<style>::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:10px}::-webkit-scrollbar-thumb:hover{background:rgba(255,255,255,0.2)}</style>""", unsafe_allow_html=True)

    def render(self):
        st.markdown(dapatkan_html_sidebar("Data"), unsafe_allow_html=True)
        self._suntik_gaya()
        self._render_header_halaman()
        self._render_filter_dan_grafik()

    def _render_header_halaman(self):
        st.markdown("""
        <div style="margin-bottom: 32px; display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 48px; color: #e2e1f0; font-weight: 600; line-height: 1.1; letter-spacing: -0.02em; margin-bottom: 8px; margin-top: 0; text-shadow: 0 0 20px rgba(164,230,255,0.4);">Eksplorasi Data Saham</h1>
                <p style="font-family: 'Space Grotesk', sans-serif; font-size: 16px; color: #bbc9cf; margin: 0; line-height: 1.6;">Lakukan pencarian dan analisis visual data historis pergerakan harga saham pilihan Anda.</p>
            </div>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

    def _render_filter_dan_grafik(self):
        kolom_ticker, kolom_periode, kolom_tombol = st.columns([2, 2, 1])

        with kolom_ticker:
            teks_ticker = st.text_input("Ticker Saham", "AAPL, MSFT, GOOGL")
            daftar_ticker = [t.strip().upper() for t in teks_ticker.split(',') if t.strip()]

        with kolom_periode:
            tahun_pilihan = st.slider("Rentang Tahun", min_value=2006, max_value=2025, value=(2006, 2025))
            tahun_mulai = tahun_pilihan[0]
            tahun_akhir = tahun_pilihan[1]

        with kolom_tombol:
            muat_data = st.button("Load Data", type="primary", use_container_width=True)

        if not muat_data and 'data_loaded' not in st.session_state:
            return

        if muat_data:
            st.session_state['data_loaded'] = True
            st.session_state['daftar_ticker'] = daftar_ticker
            st.session_state['tahun_mulai'] = tahun_mulai
            st.session_state['tahun_akhir'] = tahun_akhir

        ticker_aktif = st.session_state.get('daftar_ticker', daftar_ticker)
        tahun_mulai_aktif = st.session_state.get('tahun_mulai', tahun_mulai)
        tahun_akhir_aktif = st.session_state.get('tahun_akhir', tahun_akhir)

        # Load data menggunakan PemuatDataSaham (baca dari parquet lokal secara full)
        pemuat = PemuatDataSaham(periode='max', verbose=False)
        try:
            dict_data_raw = pemuat.muat(ticker_aktif)
            dict_data = {}
            for t, df in dict_data_raw.items():
                if not df.empty:
                    # Filter berdasarkan tahun
                    df_filtered = df[(df.index.year >= tahun_mulai_aktif) & (df.index.year <= tahun_akhir_aktif)]
                    if not df_filtered.empty:
                        dict_data[t] = df_filtered
        except Exception as e:
            st.error(f"Gagal memuat data: {e}")
            return

        if not dict_data:
            st.warning("Data tidak ditemukan untuk ticker yang dipilih.")
            return

        # ── Indikator Teknikal Toggle ──
        st.markdown("""
        <div style="margin-top: 24px; margin-bottom: 16px;">
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; font-weight: 600; color: #00d1ff; text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">Indikator Teknikal</h3>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        col_ind1, col_ind2, col_ind3, col_ind4, col_ind5, col_ind6 = st.columns(6)
        with col_ind1:
            show_bollinger = st.checkbox("Bollinger Bands", value=False)
        with col_ind2:
            show_rsi = st.checkbox("RSI (14)", value=False)
        with col_ind3:
            show_macd = st.checkbox("MACD", value=False)
        with col_ind4:
            show_atr = st.checkbox("ATR (14)", value=False)
        with col_ind5:
            show_vol = st.checkbox("Volatilitas", value=False)
        with col_ind6:
            show_ma5 = st.checkbox("MA5", value=False)

        # ── Grafik Candlestick per Ticker ──
        for ticker_nama, df_saham in dict_data.items():
            if df_saham.empty:
                continue

            st.markdown(f"""
            <div style="margin-top: 32px; margin-bottom: 8px;">
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 500; color: #e2e1f0; margin: 0; letter-spacing: 0.01em;">
                    <span style="color: #00d1ff;">$</span>{ticker_nama}
                </h3>
            </div>
            """.replace('\n', ''), unsafe_allow_html=True)

            try:
                fig = buat_grafik_candlestick(
                    df_saham,
                    kode_saham=ticker_nama,
                    judul=f"Candlestick — {ticker_nama}",
                    tampilkan_volume=True,
                    tampilkan_ma5=show_ma5,
                    tampilkan_ma20=True,
                    tampilkan_ma50=True,
                    tampilkan_bollinger=show_bollinger,
                    tampilkan_rsi=show_rsi,
                    tampilkan_macd=show_macd,
                    tampilkan_atr=show_atr,
                    tampilkan_volatilitas=show_vol,
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Gagal memuat grafik {ticker_nama}: {e}")

        # ── Grafik Komparasi (jika lebih dari 1 ticker) ──
        if len(dict_data) > 1:
            st.markdown("""
            <div style="margin-top: 48px; margin-bottom: 16px;">
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 500; color: #e2e1f0; margin: 0; letter-spacing: 0.01em;">
                    Perbandingan Antar Saham
                </h3>
                <p style="font-family: 'Space Grotesk', sans-serif; font-size: 13px; color: #bbc9cf; margin-top: 4px;">Harga dinormalisasi ke basis 100 untuk perbandingan yang adil.</p>
            </div>
            """.replace('\n', ''), unsafe_allow_html=True)

            try:
                fig_komparasi = GrafikKomparasi(
                    dict_data,
                    judul="Perbandingan Performa Saham",
                    tinggi=500,
                ).bangun()
                st.plotly_chart(fig_komparasi, use_container_width=True)
            except Exception as e:
                st.error(f"Gagal memuat grafik komparasi: {e}")


if __name__ == "__main__":
    HalamanEksplorasiData().render()