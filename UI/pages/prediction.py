import warnings
warnings.filterwarnings("ignore")

import streamlit as st
from utils.sidebar import dapatkan_html_sidebar
from utils.prediction_engine import PrediksiHargaSaham, PerbandinganInvestasi
from utils.data_handler import PengelolaDataSahamUI


class HalamanPrediksi:

    def __init__(self):
        st.set_page_config(
            page_title="Prediksi Investasi",
            page_icon="📈",
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
        st.markdown(dapatkan_html_sidebar("Prediksi"), unsafe_allow_html=True)
        self._suntik_gaya()
        self._render_header_halaman()
        self._render_input_dan_hasil()

    def _render_header_halaman(self):
        st.markdown("""
        <div style="margin-bottom: 32px; display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 48px; color: #e2e1f0; font-weight: 600; line-height: 1.1; letter-spacing: -0.02em; margin-bottom: 8px; margin-top: 0; text-shadow: 0 0 20px rgba(164,230,255,0.4);">Prediksi Investasi</h1>
                <p style="font-family: 'Space Grotesk', sans-serif; font-size: 16px; color: #bbc9cf; margin: 0; line-height: 1.6;">Masukkan budget Anda dan dapatkan rekomendasi saham terbaik beserta proyeksi harga.</p>
            </div>
            <div style="display: flex; gap: 16px;">
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; color: #a4e7f6; display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.04); backdrop-filter: blur(12px); border: 0.5px solid rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 9999px;">
                    <span class="material-symbols-outlined" style="font-size: 16px;">auto_awesome</span> AI-Powered
                </span>
            </div>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

    def _render_input_dan_hasil(self):
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Budget & Rekomendasi</h3>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        kolom_budget, kolom_jumlah, kolom_tombol = st.columns([3, 2, 2])

        with kolom_budget:
            budget = st.number_input("Budget Investasi (Rp)", min_value=1000000, value=10000000, step=1000000)
        with kolom_jumlah:
            jumlah_rekomendasi = st.number_input("Jumlah Rekomendasi Saham", min_value=1, max_value=10, value=5, step=1)
        with kolom_tombol:
            jalankan = st.button("Analisis Investasi", type="primary", use_container_width=True)

        if not jalankan:
            return

        # Get top stocks using existing scoring system
        pengelola = PengelolaDataSahamUI([])
        df_terbaik = pengelola.ambil_saham_terbaik()

        if df_terbaik.empty:
            st.warning("Data saham belum tersedia. Pastikan data sudah terunduh di folder Data/Raw.")
            return

        daftar_ticker = df_terbaik['Ticker'].head(jumlah_rekomendasi).tolist()

        # Run prediction engine
        perbandingan = PerbandinganInvestasi(daftar_ticker, budget)
        perbandingan.jalankan()

        self._render_ringkasan_rekomendasi(df_terbaik.head(jumlah_rekomendasi), budget)
        self._render_prediksi_tabs(perbandingan)
        self._render_chart_perbandingan(perbandingan)

    def _render_ringkasan_rekomendasi(self, df_top, budget):
        budget_str = f"Rp {budget:,.0f}"
        jumlah = len(df_top)
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 16px; margin-top: 32px; margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span class="material-symbols-outlined" style="font-size: 28px; color: #a4e6ff;">recommend</span>
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Top {jumlah} Saham Rekomendasi</h3>
            </div>
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em;">Budget: {budget_str}</span>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        kartu_html = ""
        for _, row in df_top.iterrows():
            ticker = row['Ticker']
            skor = row['Skor']
            risiko = row['Risiko (%)']
            ret = row['Return (%)']

            warna_ret = "#4ade80" if ret >= 0 else "#f87171"
            ikon_ret = "arrow_upward" if ret >= 0 else "arrow_downward"

            kartu_html += f"""
            <div style="background: linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(16,0,169,0.05) 100%); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 0.5px solid rgba(255,255,255,0.08); border-top-color: rgba(255,255,255,0.15); border-left-color: rgba(255,255,255,0.15); padding: 24px; border-radius: 0.75rem; position: relative; overflow: hidden; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.borderColor='rgba(164,230,255,0.3)'; this.style.boxShadow='0 10px 30px rgba(0,209,255,0.05)'" onmouseout="this.style.transform='translateY(0)'; this.style.borderColor='rgba(255,255,255,0.08)'; this.style.boxShadow='none'">
                <div style="position: absolute; top: -40px; right: -40px; width: 128px; height: 128px; background: rgba(164,230,255,0.2); border-radius: 50%; filter: blur(40px); z-index: 0;"></div>
                <div style="position: relative; z-index: 10;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <h4 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; margin: 0;">{ticker}</h4>
                        <div style="display: flex; align-items: center; gap: 4px; background: rgba(255,255,255,0.05); padding: 4px 12px; border-radius: 9999px;">
                            <span class="material-symbols-outlined" style="font-size: 16px; color: {warna_ret};">{ikon_ret}</span>
                            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; font-weight: 600; color: {warna_ret};">{ret:+.2f}%</span>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 4px 0;">Composite Score</p>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 600; color: #a4e6ff; margin: 0; text-shadow: 0 0 10px rgba(164,230,255,0.5);">{skor}<span style="font-size: 14px; color: rgba(164,230,255,0.7); margin-left: 4px;">/100</span></p>
                        </div>
                        <div>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 4px 0;">Risk Level</p>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 600; color: #e2e1f0; margin: 0;">{risiko}%</p>
                        </div>
                    </div>
                </div>
            </div>
            """

        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; margin-bottom: 32px;">
            {kartu_html}
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

    def _render_prediksi_tabs(self, perbandingan):
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 16px; margin-top: 16px; margin-bottom: 24px;">
            <span class="material-symbols-outlined" style="font-size: 28px; color: #a4e6ff;">trending_up</span>
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Proyeksi Harga & Investasi</h3>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        tab_1w, tab_1m, tab_1y = st.tabs(["📅 1 Minggu", "📅 1 Bulan", "📅 1 Tahun"])

        with tab_1w:
            self._render_kartu_prediksi(perbandingan, '1W', '1 Minggu')
        with tab_1m:
            self._render_kartu_prediksi(perbandingan, '1M', '1 Bulan')
        with tab_1y:
            self._render_kartu_prediksi(perbandingan, '1Y', '1 Tahun')

    def _render_kartu_prediksi(self, perbandingan, horizon, label):
        df = perbandingan.buat_tabel_perbandingan(horizon)
        if df.empty:
            st.info("Data prediksi tidak tersedia.")
            return

        st.markdown(f"""
        <div style="margin-bottom: 16px;">
            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; color: #bbc9cf; margin: 0;">
                Proyeksi harga & nilai investasi <strong style="color: #a4e6ff;">{label}</strong> ke depan. Budget dialokasikan merata ke setiap saham.
            </p>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        kartu_html = ""
        for _, row in df.iterrows():
            ticker = row['Ticker']
            harga_now = row['Harga Sekarang ($)']
            harga_pred = row[f'Prediksi ({horizon})']
            return_pct = row['Return (%)']
            lembar = row['Lembar Saham']
            nilai_pred = row['Nilai Prediksi ($)']
            profit = row['Profit ($)']

            if return_pct > 0:
                warna_return = "#4ade80"
                ikon_return = "arrow_upward"
            elif return_pct < 0:
                warna_return = "#f87171"
                ikon_return = "arrow_downward"
            else:
                warna_return = "#bbc9cf"
                ikon_return = "remove"

            warna_profit = "#4ade80" if profit >= 0 else "#f87171"

            kartu_html += f"""
            <div style="background: linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(16,0,169,0.05) 100%); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 0.5px solid rgba(255,255,255,0.08); border-top-color: rgba(255,255,255,0.15); padding: 24px; border-radius: 0.75rem; position: relative; overflow: hidden;">
                <div style="position: absolute; top: -30px; right: -30px; width: 100px; height: 100px; background: rgba(164,230,255,0.15); border-radius: 50%; filter: blur(35px); z-index: 0;"></div>
                <div style="position: relative; z-index: 10;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                        <h4 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; margin: 0;">{ticker}</h4>
                        <div style="display: flex; align-items: center; gap: 4px; background: rgba(255,255,255,0.05); padding: 4px 12px; border-radius: 9999px;">
                            <span class="material-symbols-outlined" style="font-size: 16px; color: {warna_return};">{ikon_return}</span>
                            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; font-weight: 600; color: {warna_return};">{return_pct:+.2f}%</span>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
                        <div>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 4px 0;">Harga Sekarang</p>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 500; color: #e2e1f0; margin: 0;">Rp {harga_now:,.0f}</p>
                        </div>
                        <div>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 4px 0;">Prediksi {label}</p>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 500; color: #a4e6ff; margin: 0; text-shadow: 0 0 10px rgba(164,230,255,0.4);">Rp {harga_pred:,.0f}</p>
                        </div>
                    </div>
                    <div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 12px; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;">
                        <div>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 10px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 2px 0;">Lembar</p>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; color: #e2e1f0; margin: 0;">{lembar:,}</p>
                        </div>
                        <div>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 10px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 2px 0;">Nilai Investasi</p>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; color: #e2e1f0; margin: 0;">Rp {nilai_pred:,.0f}</p>
                        </div>
                        <div>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 10px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 2px 0;">Profit/Loss</p>
                            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; font-weight: 600; color: {warna_profit}; margin: 0;">Rp {profit:+,.0f}</p>
                        </div>
                    </div>
                </div>
            </div>
            """

        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 16px;">
            {kartu_html}
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

    def _render_chart_perbandingan(self, perbandingan):
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 16px; margin-top: 32px; margin-bottom: 24px;">
            <span class="material-symbols-outlined" style="font-size: 20px; color: #a4e6ff;">bar_chart</span>
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Perbandingan Proyeksi Return</h3>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        df_chart = perbandingan.buat_data_chart()
        if df_chart.empty:
            st.info("Data chart tidak tersedia.")
            return

        st.bar_chart(df_chart.set_index('Ticker'))


if __name__ == "__main__":
    HalamanPrediksi().render()
