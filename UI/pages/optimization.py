import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import streamlit.components.v1 as components
from utils.portfolio_model import OptimasiPortofolio
from utils.sidebar import dapatkan_html_sidebar


class HalamanOptimasi:

    def __init__(self):
        st.set_page_config(
            page_title="Optimization",
            page_icon="⚙️",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    def _suntik_gaya(self):
        st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>', unsafe_allow_html=True)
        st.markdown('<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>', unsafe_allow_html=True)
        
        # Ambient Orbs Background & Main App background
        st.markdown("""<style>.stApp{background-color:#11131d;color:#e2e1f0;font-family:'Space Grotesk',sans-serif;}.stApp::before{content:'';position:fixed;top:0;left:0;width:40vw;height:40vw;background:radial-gradient(circle, rgba(0, 209, 255, 0.15) 0%, transparent 70%);border-radius:50%;z-index:-1;pointer-events:none;}.stApp::after{content:'';position:fixed;bottom:0;right:0;width:50vw;height:50vw;background:radial-gradient(circle, rgba(192, 193, 255, 0.1) 0%, transparent 70%);border-radius:50%;z-index:-1;pointer-events:none;}[data-testid="stHeader"]{display:none!important}.block-container{padding-top:2rem!important; padding-bottom:2rem!important;}</style>""", unsafe_allow_html=True)
        
        # Glass Cards
        st.markdown("""<style>[data-testid="stHorizontalBlock"],[data-testid="stArrowVegaLiteChart"],[data-testid="stDataFrame"],[data-testid="stTabs"]{background:linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(192,193,255,0.05) 100%);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:0.5px solid rgba(255,255,255,0.1);border-top-color:rgba(255,255,255,0.2);border-left-color:rgba(255,255,255,0.2);box-shadow:0 20px 40px rgba(0,0,0,0.3);border-radius:0.75rem;padding:24px;margin-bottom:24px;position:relative}</style>""", unsafe_allow_html=True)
        
        # Glass Inputs
        st.markdown("""<style>.stTextInput input,.stNumberInput input{background:rgba(255,255,255,0.04)!important;border:0.5px solid rgba(255,255,255,0.1)!important;color:#e2e1f0!important;border-radius:0.5rem!important;font-family:'Space Grotesk',sans-serif!important;padding:12px!important;transition:all 0.3s ease!important}.stTextInput input:focus,.stNumberInput input:focus{border-color:rgba(0,209,255,0.5)!important;box-shadow:0 0 15px rgba(0,209,255,0.1)!important;background:rgba(255,255,255,0.08)!important}</style>""", unsafe_allow_html=True)
        
        # MultiSelect & SelectBox
        st.markdown("""<style>.stMultiSelect div[data-baseweb="select"]{background:rgba(255,255,255,0.04)!important;border:0.5px solid rgba(255,255,255,0.1)!important;border-radius:0.5rem!important}.stMultiSelect span[data-baseweb="tag"]{background-color:rgba(0,209,255,0.1)!important;border:1px solid rgba(0,209,255,0.3)!important;color:#00d1ff!important;border-radius:0.25rem!important;font-family:'Space Grotesk',sans-serif!important}</style>""", unsafe_allow_html=True)
        
        # Radio & Labels
        st.markdown("""<style>.stRadio label div{color:#bbc9cf!important;font-family:'Space Grotesk',sans-serif!important;font-size:14px!important}[data-testid="stWidgetLabel"]{font-family:'Space Grotesk',sans-serif!important;text-transform:uppercase!important;letter-spacing:0.05em!important;color:#bbc9cf!important;font-size:12px!important;font-weight:600!important}[data-testid="stWidgetLabel"] p{font-size:12px!important;font-weight:600!important}</style>""", unsafe_allow_html=True)
        
        # Glass Buttons
        st.markdown("""<style>[data-testid="stButton"] button{background:rgba(255,255,255,0.04)!important;backdrop-filter:blur(12px)!important;border:0.5px solid rgba(255,255,255,0.1)!important;border-top-color:rgba(255,255,255,0.2)!important;color:#e2e1f0!important;border-radius:0.5rem!important;font-family:'Space Grotesk',sans-serif!important;text-transform:uppercase!important;letter-spacing:0.05em!important;font-weight:600!important;padding:12px 24px!important;height:auto!important;transition:all 0.3s ease!important;margin-top:28px!important}[data-testid="stButton"] button:hover{background:rgba(255,255,255,0.1)!important;border-color:rgba(0,209,255,0.5)!important;color:#00d1ff!important;box-shadow:0 0 15px rgba(0,209,255,0.2)!important}</style>""", unsafe_allow_html=True)
        
        # Metrics
        st.markdown("""<style>[data-testid="metric-container"]{border:none;padding:16px}[data-testid="stMetricValue"]{font-family:'Space Grotesk',sans-serif!important;font-size:48px!important;color:#a4e6ff!important;font-weight:600!important;line-height:1.1!important;letter-spacing:-0.02em!important;text-shadow:0 0 20px rgba(164,230,255,0.4)!important}[data-testid="stMetricLabel"]{font-family:'Space Grotesk',sans-serif!important;color:#bbc9cf!important;text-transform:uppercase!important;letter-spacing:0.05em!important;font-size:12px!important;font-weight:600!important}</style>""", unsafe_allow_html=True)
        
        # Tabs
        st.markdown("""<style>button[data-baseweb="tab"]{font-family:'Space Grotesk',sans-serif!important;text-transform:uppercase!important;letter-spacing:0.05em!important;color:#bbc9cf!important;background-color:transparent!important;font-weight:600!important;font-size:14px!important}button[data-baseweb="tab"][aria-selected="true"]{color:#00d1ff!important;border-bottom-color:#00d1ff!important}</style>""", unsafe_allow_html=True)
        
        # Scrollbars
        st.markdown("""<style>::-webkit-scrollbar{width:4px;height:4px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:4px}::-webkit-scrollbar-thumb:hover{background:rgba(255,255,255,0.2)}</style>""", unsafe_allow_html=True)

    def render(self):
        st.markdown(dapatkan_html_sidebar("Optimize"), unsafe_allow_html=True)
        self._suntik_gaya()
        self._render_bilah_atas()
        self._render_header_halaman()
        self._render_parameter_dan_hasil()

    def _render_bilah_atas(self):
        st.markdown("""
        <header style="display: flex; justify-content: space-between; align-items: center; width: 100%; border-bottom: 1px solid rgba(255,255,255,0.1); background-color: rgba(17,19,29,0.1); backdrop-filter: blur(12px); padding: 16px 0; margin-top: -16px; z-index: 40; position: relative; margin-bottom: 32px;">
            <div style="display: flex; align-items: center; gap: 8px; font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; color: #bbc9cf;">
                <span style="width: 6px; height: 6px; border-radius: 50%; background-color: #4ade80; box-shadow: 0 0 5px rgba(74,222,128,0.5);"></span>
                <span>System Status: Optimal</span>
            </div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <button style="background: transparent; border: none; color: #bbc9cf; cursor: pointer; transition: color 0.3s; padding: 0; display: flex;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#bbc9cf'">
                    <span class="material-symbols-outlined" style="font-size: 20px;">notifications</span>
                </button>
                <button style="background: transparent; border: none; color: #bbc9cf; cursor: pointer; transition: color 0.3s; padding: 0; display: flex;" onmouseover="this.style.color='white'" onmouseout="this.style.color='#bbc9cf'">
                    <span class="material-symbols-outlined" style="font-size: 20px;">account_circle</span>
                </button>
                <button style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; text-transform: uppercase; padding: 8px 24px; border: 1px solid #a4e6ff; color: #a4e6ff; background: transparent; border-radius: 0.5rem; cursor: pointer; letter-spacing: 0.05em; transition: all 0.3s; margin-left: 16px;" onmouseover="this.style.backgroundColor='rgba(164,230,255,0.1)'" onmouseout="this.style.backgroundColor='transparent'">
                    Deploy Strategy
                </button>
            </div>
        </header>
        """.replace('\n', ''), unsafe_allow_html=True)

    def _render_header_halaman(self):
        st.markdown("""
        <div style="margin-bottom: 32px; display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 48px; color: #e2e1f0; font-weight: 600; line-height: 1.1; letter-spacing: -0.02em; margin-bottom: 8px; margin-top: 0; text-shadow: 0 0 20px rgba(164,230,255,0.4);">Optimization Results</h1>
                <p style="font-family: 'Space Grotesk', sans-serif; font-size: 16px; color: #bbc9cf; margin: 0; line-height: 1.6;">Global Equities Core - Mean Variance Model</p>
            </div>
            <div style="display: flex; gap: 16px;">
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; color: #a4e7f6; display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.04); backdrop-filter: blur(12px); border: 0.5px solid rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 9999px;">
                    <span class="material-symbols-outlined" style="font-size: 16px;">check_circle</span> Converged
                </span>
            </div>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

    def _render_parameter_dan_hasil(self):
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Parameter Input</h3>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        kolom_saham, kolom_metode, kolom_modal, kolom_tombol = st.columns([3, 2, 2, 2])

        with kolom_saham:
            daftar_tersedia = st.session_state.get('data_tersedia', ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA'])
            if not daftar_tersedia:
                daftar_tersedia = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA']

            daftar_ticker = st.multiselect(
                "Pilih Saham",
                daftar_tersedia,
                default=daftar_tersedia[:2] if len(daftar_tersedia) >= 2 else daftar_tersedia
            )
        with kolom_metode:
            metode = st.radio("Metode", ('Maximize Sharpe Ratio', 'Minimize Risk'))
        with kolom_modal:
            modal = st.number_input("Modal Awal (Rp)", min_value=1000000, value=10000000, step=1000000)
        with kolom_tombol:
            jalankan = st.button("Jalankan Optimasi", type="primary", use_container_width=True)

        if not jalankan:
            return

        if not daftar_ticker:
            st.warning("Pilih minimal 1 saham untuk dioptimasi.")
            return

        optimasi = OptimasiPortofolio(daftar_ticker, modal)
        metrik = optimasi.ambil_metrik_kpi()

        self._render_metrik(metrik)
        self._render_tab_hasil(optimasi)
        self._render_tabel_rekomendasi(optimasi)

    def _render_metrik(self, metrik: dict):
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; margin-top: 32px; margin-bottom: 16px;">
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Ringkasan Metrik</h3>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        kolom1, kolom2, kolom3 = st.columns(3)
        kolom1.metric("Proyeksi Keuntungan", metrik["proyeksi_return"])
        kolom2.metric("Volatilitas", metrik["volatilitas"])
        kolom3.metric("Rasio Sharpe", metrik["rasio_sharpe"])

    def _render_tab_hasil(self, optimasi: OptimasiPortofolio):
        tab_alokasi, tab_kinerja, tab_frontier = st.tabs(["Alokasi", "Kinerja", "Efficient Frontier"])

        with tab_alokasi:
            st.markdown("""
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 16px; margin-bottom: 24px;">
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Target Asset Allocation</h3>
            </div>
            """.replace('\n', ''), unsafe_allow_html=True)

            df_bobot = optimasi.hitung_bobot_optimal()
            st.bar_chart(df_bobot.set_index('Saham'))

        with tab_kinerja:
            st.write("Visualisasi Backtesting Portofolio.")

        with tab_frontier:
            st.write("Visualisasi Efficient Frontier.")

    def _render_tabel_rekomendasi(self, optimasi: OptimasiPortofolio):
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 16px; margin-top: 32px; margin-bottom: 24px;">
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Action Plan (Rekomendasi)</h3>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        df_laporan = optimasi.buat_laporan_alokasi()

        st.dataframe(
            df_laporan.style.format({'Alokasi (Rp)': 'Rp {:,.0f}'}),
            width='stretch',
            hide_index=True
        )


if __name__ == "__main__":
    HalamanOptimasi().render()