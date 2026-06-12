import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import streamlit.components.v1 as components
from UI.utils.data_handler import PengelolaDataSahamUI
from UI.utils.sidebar import dapatkan_html_sidebar


class HalamanSahamTerbaik:

    DAFTAR_IKON = ["military_tech", "trending_up", "show_chart"]

    def __init__(self):
        st.set_page_config(
            page_title="Top Stocks",
            page_icon="⭐",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    def _suntik_gaya(self):
        st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>', unsafe_allow_html=True)
        st.markdown('<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>', unsafe_allow_html=True)
        
        # Ambient Orbs Background & Main App background
        st.markdown("""<style>.stApp{background-color:#0c0e17;color:#e2e1f0;font-family:'Space Grotesk',sans-serif;}.stApp::before{content:'';position:fixed;top:-10%;left:-5%;width:40vw;height:40vw;background:rgba(164,230,255,0.05);filter:blur(100px);border-radius:50%;z-index:-1;pointer-events:none;}.stApp::after{content:'';position:fixed;bottom:-20%;right:-10%;width:50vw;height:50vw;background:rgba(49,49,192,0.05);filter:blur(120px);border-radius:50%;z-index:-1;pointer-events:none;}[data-testid="stHeader"]{display:none!important}.block-container{padding-top:2rem!important; padding-bottom:2rem!important;}</style>""", unsafe_allow_html=True)
        
        # Glass Panels for Charts/DataFrames
        st.markdown("""<style>[data-testid="stArrowVegaLiteChart"],[data-testid="stDataFrame"]{background:rgba(255,255,255,0.03);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:0.5px solid rgba(255,255,255,0.1);border-top-color:rgba(255,255,255,0.2);border-left-color:rgba(255,255,255,0.2);box-shadow:0 20px 40px rgba(0,0,0,0.3);padding:24px;border-radius:0.75rem;}</style>""", unsafe_allow_html=True)
        
        # Scrollbars
        st.markdown("""<style>::-webkit-scrollbar{width:4px;height:4px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:4px}::-webkit-scrollbar-thumb:hover{background:rgba(255,255,255,0.2)}</style>""", unsafe_allow_html=True)

    def render(self):
        st.markdown(dapatkan_html_sidebar("Top Stocks"), unsafe_allow_html=True)
        self._suntik_gaya()

        self._render_header_halaman()
        self._render_konten_utama()



    def _render_header_halaman(self):
        st.markdown("""
        <div style="margin-bottom: 48px; display: flex; flex-direction: column; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 6px; height: 32px; background-color: #a4e6ff; border-radius: 9999px; box-shadow: 0 0 10px rgba(164,230,255,0.5);"></div>
                <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 48px; color: #e2e1f0; font-weight: 600; line-height: 1.1; letter-spacing: -0.02em; margin: 0; text-shadow: 0 0 20px rgba(164,230,255,0.4);">Top 5 Saham Pilihan</h1>
            </div>
            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 16px; color: #bbc9cf; max-width: 42rem; margin: 0; line-height: 1.6; letter-spacing: 0.01em;">
                Pemilihan saham secara otomatis melalui sistem perankingan algoritma yang menyeimbangkan pergerakan harga, valuasi, serta tingkat risiko selama 30 hari ke belakang.
            </p>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

    def _render_konten_utama(self):
        pengelola = PengelolaDataSahamUI([])

        with st.spinner("Mengunduh data live dari Yahoo Finance..."):
            df_terbaik = pengelola.ambil_saham_terbaik_live()

        if df_terbaik.empty:
            st.warning("Gagal mengunduh data live saham dari Yahoo Finance. Silakan periksa koneksi internet Anda.")
            return

        st.markdown('<div style="margin-bottom: 32px;"></div>', unsafe_allow_html=True)

        self._render_kartu_podium(df_terbaik)
        self._render_grafik_dan_tabel(df_terbaik)

    def _buat_html_kartu(self, indeks: int, ticker: str, skor: float, risiko: float) -> str:
        rank = indeks + 1
        
        bg_color = "linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(16,0,169,0.05) 100%)"
        highlight_color = "#a4e6ff" # primary
        highlight_bg = "rgba(164,230,255,0.2)"
        bar_color = "#a4e6ff"
        glow = "text-shadow: 0 0 10px rgba(164,230,255,0.5);"
        bar_glow = "box-shadow: 0 0 10px rgba(164,230,255,0.8);"
        radial_bg = '<div style="position: absolute; top: -40px; right: -40px; width: 128px; height: 128px; background: rgba(164,230,255,0.2); border-radius: 50%; filter: blur(40px); z-index: 0;"></div>'

        return f"""
        <div style="background: {bg_color}; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 0.5px solid rgba(255,255,255,0.08); border-top-color: rgba(255,255,255,0.15); border-left-color: rgba(255,255,255,0.15); padding: 32px; border-radius: 0.75rem; position: relative; overflow: hidden; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.borderColor='rgba(164,230,255,0.3)'; this.style.boxShadow='0 10px 30px rgba(0,209,255,0.05)'" onmouseout="this.style.transform='translateY(0)'; this.style.borderColor='rgba(255,255,255,0.08)'; this.style.boxShadow='none'">
            {radial_bg}
            <div style="position: relative; z-index: 10;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="width: 32px; height: 32px; border-radius: 50%; background: {highlight_bg}; border: 1px solid {highlight_color}4d; display: flex; align-items: center; justify-content: center; font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; color: {highlight_color};">#{rank}</span>
                        <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 500; color: #e2e1f0; margin: 0; letter-spacing: -0.01em;">{ticker}</h3>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; gap: 16px;">
                    <div>
                        <p style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em; margin: 0 0 4px 0;">Composite Score</p>
                        <div style="display: flex; align-items: flex-end; gap: 8px;">
                            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 48px; font-weight: 600; color: #a4e6ff; line-height: 1.1; letter-spacing: -0.02em; {glow}">{skor}</span>
                            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 16px; color: rgba(164,230,255,0.7); margin-bottom: 8px;">/100</span>
                        </div>
                    </div>
                    <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.1); border-radius: 9999px; overflow: hidden;">
                        <div style="height: 100%; background: {bar_color}; width: {skor}%; border-radius: 9999px; {bar_glow}"></div>
                    </div>
                    <div style="margin-top: 8px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; color: #bbc9cf; text-transform: uppercase; letter-spacing: 0.05em;">Risk: {risiko}%</span>
                    </div>
                </div>
            </div>
        </div>
        """

    def _render_kartu_podium(self, df_terbaik):
        jumlah_kartu = min(3, len(df_terbaik))
        kartu_html = "".join(
            self._buat_html_kartu(
                i,
                df_terbaik['Ticker'].iloc[i],
                df_terbaik['Skor'].iloc[i],
                df_terbaik['Risiko (%)'].iloc[i]
            )
            for i in range(jumlah_kartu)
        )

        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-bottom: 64px;">
            {kartu_html}
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

    def _render_grafik_dan_tabel(self, df_terbaik):
        kolom_kiri, kolom_kanan = st.columns([1, 1])

        with kolom_kiri:
            st.markdown("""
            <div style="margin-bottom: 16px;">
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Momentum vs Value</h3>
                <p style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; color: #bbc9cf; margin: 4px 0 0 0;">Grafik di bawah menunjukkan imbal hasil / <b>Return (%)</b> (Sumbu Y) per masing-masing ticker saham.</p>
            </div>
            """.replace('\n', ''), unsafe_allow_html=True)
            data_grafik = df_terbaik.set_index('Ticker')[['Return (%)']]
            st.bar_chart(data_grafik)

        with kolom_kanan:
            st.markdown("""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Data Output</h3>
            </div>
            """.replace('\n', ''), unsafe_allow_html=True)
            st.dataframe(df_terbaik[['Ticker', 'Risiko (%)', 'Skor']], hide_index=True, width='stretch')


if __name__ == "__main__":
    HalamanSahamTerbaik().render()