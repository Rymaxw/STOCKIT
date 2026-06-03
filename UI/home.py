import warnings
warnings.filterwarnings("ignore")

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import streamlit.components.v1 as components
from utils.sidebar import dapatkan_html_sidebar
from Utils.st_dataloader import inisialisasi_sistem


class HalamanBeranda:

    def __init__(self):
        st.set_page_config(
            page_title="STOCKIT - Stock Portfolio",
            page_icon="🏠",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

        folder_utama = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        inisialisasi_sistem(folder_utama)

    def _suntik_gaya(self):
        st.markdown('<style>#MainMenu{visibility:hidden}footer{visibility:hidden}</style>', unsafe_allow_html=True)
        st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>', unsafe_allow_html=True)
        st.markdown('<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>', unsafe_allow_html=True)
        
        # Base Theme Styles
        st.markdown("""
        <style>
            .stApp {
                background-color: #11131d;
                background-image: 
                    radial-gradient(circle at 15% 50%, rgba(0, 209, 255, 0.05) 0%, transparent 50%),
                    radial-gradient(circle at 85% 30%, rgba(192, 193, 255, 0.05) 0%, transparent 50%);
                background-attachment: fixed;
                color: #e2e1f0;
                font-family: 'Space Grotesk', sans-serif;
                min-height: 100vh;
            }
            [data-testid="stHeader"] {display:none!important}
            .block-container {padding-top:2rem!important; padding-bottom:2rem!important;}
        </style>
        """, unsafe_allow_html=True)

        # Button Styles (Glow Button)
        st.markdown("""
        <style>
            [data-testid="stButton"] button {
                background: linear-gradient(135deg, #a4e6ff, #b7eaff) !important;
                color: #001f28 !important;
                border: none !important;
                border-radius: 8px !important;
                font-family: 'Space Grotesk', sans-serif !important;
                font-weight: 600 !important;
                padding: 12px 24px !important;
                height: auto !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 0 20px rgba(0, 209, 255, 0.2) !important;
            }
            [data-testid="stButton"] button p {
                font-size: 14px !important;
                margin: 0 !important;
                color: #001f28 !important;
                font-weight: 600 !important;
            }
            [data-testid="stButton"] button:hover {
                box-shadow: 0 0 30px rgba(0, 209, 255, 0.4) !important;
                transform: translateY(-1px) !important;
                background: linear-gradient(135deg, #b7eaff, #a4e6ff) !important;
            }
            ::-webkit-scrollbar {width: 8px; height: 8px;}
            ::-webkit-scrollbar-track {background: #11131d;}
            ::-webkit-scrollbar-thumb {background: #3c494e; border-radius: 4px;}
            ::-webkit-scrollbar-thumb:hover {background: #4cd6ff;}
        </style>
        """, unsafe_allow_html=True)

    def render(self):
        self._suntik_gaya()

        st.markdown(dapatkan_html_sidebar("Home"), unsafe_allow_html=True)

        # Header Section
        st.markdown("""
        <header style="display: flex; justify-content: space-between; align-items: center; width: 100%; border-bottom: 1px solid rgba(255, 255, 255, 0.1); background-color: rgba(17, 19, 29, 0.1); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); padding: 16px 0; margin-top: -16px; z-index: 40; position: relative; margin-bottom: 32px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; font-weight: 700; color: #00d1ff; text-transform: uppercase; letter-spacing: 0.1em; margin: 0;">Overview</h2>
            </div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <button style="color: #bbc9cf; background: transparent; border: none; cursor: pointer; padding: 8px; border-radius: 50%; transition: all 0.3s; display: flex; align-items: center; justify-content: center;" onmouseover="this.style.backgroundColor='rgba(0, 209, 255, 0.1)'; this.style.color='#00d1ff'" onmouseout="this.style.backgroundColor='transparent'; this.style.color='#bbc9cf'">
                    <span class="material-symbols-outlined">notifications</span>
                </button>
                <button style="color: #bbc9cf; background: transparent; border: none; cursor: pointer; padding: 8px; border-radius: 50%; transition: all 0.3s; display: flex; align-items: center; justify-content: center;" onmouseover="this.style.backgroundColor='rgba(0, 209, 255, 0.1)'; this.style.color='#00d1ff'" onmouseout="this.style.backgroundColor='transparent'; this.style.color='#bbc9cf'">
                    <span class="material-symbols-outlined">account_circle</span>
                </button>
                <button style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; padding: 8px 16px; border: 1px solid rgba(0, 209, 255, 0.3); color: #00d1ff; background: rgba(0, 209, 255, 0.05); cursor: pointer; border-radius: 9999px; transition: all 0.3s; margin-left: 8px;" onmouseover="this.style.background='rgba(0, 209, 255, 0.1)'" onmouseout="this.style.background='rgba(0, 209, 255, 0.05)'">
                    Deploy Strategy
                </button>
            </div>
        </header>
        """.replace('\n', ''), unsafe_allow_html=True)

        # Title Hero
        st.markdown("""
        <div style="margin-bottom: 48px;">
            <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 48px; font-weight: 600; color: #e2e1f0; margin-bottom: 12px; display: flex; align-items: center; gap: 16px; letter-spacing: -0.02em; margin-top: 0;">
                STOCKIT
                <span class="material-symbols-outlined" style="color: #00d1ff; font-size: 40px;">dataset</span>
            </h1>
            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 18px; color: #bbc9cf; margin: 0; font-weight: 400;">
                Precision Data Science for Stock Portfolio Optimization
            </p>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        # Layout Columns
        # Padding applied via columns in streamlit
        st.markdown('<div>', unsafe_allow_html=True)
        kolom_kiri, spacer, kolom_kanan = st.columns([5, 0.2, 4])

        with kolom_kiri:
            self._render_kotak_mulai_cepat()

        with kolom_kanan:
            self._render_kartu_eksplorasi()
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Render status at the bottom corner
        st.markdown('<div style="margin-top: 48px;">', unsafe_allow_html=True)
        self._render_status_sistem()
        st.markdown('</div>', unsafe_allow_html=True)

    def _render_kotak_mulai_cepat(self):
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); border-top: 1px solid rgba(255, 255, 255, 0.2); border-left: 1px solid rgba(255, 255, 255, 0.2); border-radius: 12px; padding: 32px; margin-bottom: 24px; position: relative; overflow: hidden; height: 100%;">
            <div style="position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(0, 209, 255, 0.1); border-radius: 50%; filter: blur(40px); pointer-events: none;"></div>
            
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
                <span class="material-symbols-outlined" style="color: #00d1ff; font-size: 28px;">tune</span>
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; margin: 0;">Mulai Cepat</h3>
            </div>
            
            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 16px; color: #bbc9cf; margin-bottom: 32px; line-height: 1.6; font-weight: 400;">
                Aplikasi ini membantu merancang portofolio saham menggunakan pendekatan kuantitatif modern. 
                Masuk ke dasbor optimasi untuk mengatur parameter simulasi algoritma Anda.
            </p>
            
            <div style="margin-top: 16px; display: flex; justify-content: flex-end;">
            </div>
        </div>
        <style>
        /* CSS to hide streamlit button default padding issues and position it correctly */
        </style>
        """.replace('\n', ''), unsafe_allow_html=True)

        # Place the button
        if st.button("Buka Dasbor Optimasi", use_container_width=False):
            st.switch_page("pages/optimization.py")

    def _render_kartu_eksplorasi(self):
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); border-top: 1px solid rgba(255, 255, 255, 0.2); border-left: 1px solid rgba(255, 255, 255, 0.2); border-radius: 12px; padding: 24px; display: flex; flex-direction: column; height: 100%;">
            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 16px;">Tersedia</p>
            
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.05); border-left: 2px solid #00d1ff; border-radius: 8px; padding: 20px; display: flex; align-items: flex-start; gap: 16px; cursor: pointer; transition: all 0.3s; margin-bottom: 24px;" onmouseover="this.style.backgroundColor='rgba(255, 255, 255, 0.08)'" onmouseout="this.style.backgroundColor='rgba(255, 255, 255, 0.03)'">
                <div style="padding: 12px; background: rgba(0, 209, 255, 0.1); border-radius: 8px; color: #00d1ff; display: flex; align-items: center; justify-content: center;">
                    <span class="material-symbols-outlined" style="font-size: 24px;">timeline</span>
                </div>
                <div style="flex: 1;">
                    <h4 style="font-family: 'Space Grotesk', sans-serif; font-size: 16px; font-weight: 600; color: #e2e1f0; margin: 0 0 4px 0;">Eksplorasi Data</h4>
                    <p style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 400; color: #bbc9cf; margin: 0;">Analisis pergerakan harga saham secara mendalam dan visual.</p>
                </div>
            </div>
            
            <div style="flex: 1;"></div>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        if st.button("Eksplorasi Market Data Sekarang", use_container_width=True):
            st.switch_page("pages/data_exploration.py")

    def _render_status_sistem(self):
        st.markdown("""
        <div style="display: flex; gap: 16px; justify-content: flex-end;">
            <div style="background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 9999px; padding: 8px 16px; display: flex; align-items: center; gap: 8px;">
                <div style="width: 8px; height: 8px; background-color: #4cd6ff; border-radius: 50%; box-shadow: 0 0 8px #4cd6ff; animation: pulse 2s infinite;"></div>
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em;">Engine: Online</span>
            </div>
            <div style="background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 9999px; padding: 8px 16px; display: flex; align-items: center; gap: 8px;">
                <div style="width: 8px; height: 8px; background-color: #4cd6ff; border-radius: 50%; box-shadow: 0 0 8px #4cd6ff; animation: pulse 2s infinite; animation-delay: 0.5s;"></div>
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em;">Data Feed: Syncing</span>
            </div>
        </div>
        <style>
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.4; }
            100% { opacity: 1; }
        }
        </style>
        """.replace('\n', ''), unsafe_allow_html=True)


if __name__ == "__main__":
    aplikasi = HalamanBeranda()
    aplikasi.render()