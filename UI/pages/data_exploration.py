import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import datetime
import plotly.express as px
from utils.data_handler import PengelolaDataSahamUI
from utils.sidebar import dapatkan_html_sidebar


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
        
        # Glass Panels
        st.markdown("""<style>[data-testid="stHorizontalBlock"]{background:rgba(26,27,37,0.4);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,0.05);box-shadow:0 8px 32px 0 rgba(0,0,0,0.3);border-radius:1rem;padding:24px;margin-bottom:24px}[data-testid="stArrowVegaLiteChart"],[data-testid="stDataFrame"]{background:rgba(26,27,37,0.4);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,0.05);box-shadow:0 8px 32px 0 rgba(0,0,0,0.3);border-radius:1rem;padding:24px;margin-top:16px}</style>""", unsafe_allow_html=True)
        
        # Glass Inputs
        st.markdown("""<style>.stTextInput input,.stDateInput input{background:rgba(0,0,0,0.2)!important;border:1px solid rgba(255,255,255,0.1)!important;color:#e2e1f0!important;border-radius:0.5rem!important;font-family:'Inter',sans-serif!important;padding:12px!important;transition:all 0.3s ease!important}.stTextInput input:focus,.stDateInput input:focus{border-color:rgba(0,209,255,0.5)!important;box-shadow:0 0 15px rgba(0,209,255,0.1)!important;background:rgba(0,0,0,0.3)!important}</style>""", unsafe_allow_html=True)
        
        # Labels
        st.markdown("""<style>[data-testid="stWidgetLabel"]{font-family:'Inter',sans-serif!important;color:#bbc9cf!important;font-size:11px!important}[data-testid="stWidgetLabel"] p{font-size:11px!important}</style>""", unsafe_allow_html=True)
        
        # Glass Buttons
        st.markdown("""<style>[data-testid="stButton"] button{background:linear-gradient(135deg, rgba(0,209,255,0.1), rgba(0,103,127,0.2))!important;border:1px solid rgba(0,209,255,0.3)!important;color:#00d1ff!important;border-radius:0.5rem!important;font-family:'Inter',sans-serif!important;font-weight:500!important;padding:12px 24px!important;height:auto!important;transition:all 0.3s ease!important;backdrop-filter:blur(8px)!important;margin-top:28px!important}[data-testid="stButton"] button:hover{background:linear-gradient(135deg, rgba(0,209,255,0.2), rgba(0,103,127,0.3))!important;border-color:rgba(0,209,255,0.6)!important;box-shadow:0 0 20px rgba(0,209,255,0.2)!important;transform:translateY(-1px)!important}</style>""", unsafe_allow_html=True)
        
        # Scrollbars
        st.markdown("""<style>::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:10px}::-webkit-scrollbar-thumb:hover{background:rgba(255,255,255,0.2)}</style>""", unsafe_allow_html=True)

    def render(self):
        st.markdown(dapatkan_html_sidebar("Data"), unsafe_allow_html=True)
        self._suntik_gaya()
        self._render_bilah_atas()
        self._render_header_halaman()
        self._render_filter_dan_grafik()

    def _render_bilah_atas(self):
        st.markdown("""
        <header style="display: flex; justify-content: space-between; align-items: center; width: 100%; border-bottom: 1px solid rgba(255,255,255,0.05); padding: 16px 0; margin-top: -16px; z-index: 40; position: relative; margin-bottom: 32px;">
            <div style="display: flex; align-items: center; gap: 8px; font-family: 'Inter', sans-serif; font-size: 12px; color: #bbc9cf;">
                <span style="width: 6px; height: 6px; border-radius: 50%; background-color: #4ade80; box-shadow: 0 0 5px rgba(74,222,128,0.5);"></span>
                <span>System Status: Optimal</span>
            </div>
            <div style="display: flex; align-items: center; gap: 20px; color: #bbc9cf;">
                <span class="material-symbols-outlined" style="cursor: pointer; font-size: 20px; transition: color 0.3s;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#bbc9cf'">notifications</span>
                <span class="material-symbols-outlined" style="cursor: pointer; font-size: 20px; transition: color 0.3s;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#bbc9cf'">settings</span>
            </div>
        </header>
        """.replace('\n', ''), unsafe_allow_html=True)

    def _render_header_halaman(self):
        st.markdown("""
        <div style="margin-bottom: 32px;">
            <h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 30px; font-weight: 300; color: white; letter-spacing: -0.02em; margin-bottom: 4px; margin-top: 0;">Eksplorasi Data Saham</h2>
            <p style="font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 500; color: rgba(187, 201, 207, 0.7); margin: 0;">QUERY // DATA_PASAR_US // HISTORIS</p>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

    def _render_filter_dan_grafik(self):
        kolom_ticker, kolom_tanggal, kolom_tombol = st.columns([2, 2, 1])

        with kolom_ticker:
            teks_ticker = st.text_input("Ticker Saham", "AAPL, MSFT, GOOGL")
            daftar_ticker = [t.strip() for t in teks_ticker.split(',')]

        with kolom_tanggal:
            tanggal_awal = datetime.date(2006, 1, 1)
            tanggal_batas = datetime.date(2025, 12, 31)
            rentang_tanggal = st.date_input("Rentang Waktu", value=(tanggal_awal, tanggal_batas), min_value=tanggal_awal, max_value=tanggal_batas)

        with kolom_tombol:
            muat_data = st.button("Load Data", type="primary", use_container_width=True)

        if not muat_data:
            return

        if len(rentang_tanggal) != 2:
            st.error("⚠️ Pilih tanggal awal dan akhir terlebih dahulu.")
            return

        tanggal_mulai, tanggal_akhir = rentang_tanggal

        pengelola = PengelolaDataSahamUI(daftar_ticker)
        df_historis = pengelola.ambil_data_historis(tanggal_mulai, tanggal_akhir)

        if df_historis.empty:
            st.warning("Data tidak ditemukan.")
            return

        self._render_grafik_harga(df_historis)

    def _render_grafik_harga(self, df_historis):
        st.markdown("""
        <div style="margin-top: 32px; margin-bottom: 16px;">
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 500; color: white; margin: 0; letter-spacing: 0.025em;">Pergerakan Harga Saham</h3>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        grafik = px.line(
            df_historis, x=df_historis.index, y=df_historis.columns,
            labels={'value': 'Harga (USD)', 'index': 'Tanggal', 'variable': 'Ticker'},
            template='plotly_dark'
        )

        grafik.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif"),
            xaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.05)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.05)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified",
            margin=dict(l=0, r=0, t=0, b=0)
        )

        st.markdown('<div style="background: rgba(26, 27, 37, 0.4); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); border-radius: 1rem; padding: 24px;">', unsafe_allow_html=True)
        st.plotly_chart(grafik, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    HalamanEksplorasiData().render()