import streamlit as st
import streamlit.components.v1 as components
from utils.data_handler import StockDataHandler
from utils.sidebar import get_sidebar_html

class TopStocksPage:
    def __init__(self):
        st.set_page_config(
            page_title="Top Stocks",
            page_icon="⭐",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    def render(self):
        # Inject custom sidebar
        st.markdown(get_sidebar_html("Top Stocks"), unsafe_allow_html=True)

        # Inject Custom CSS
        st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Space+Mono:wght@400;700&family=Geist:wght@400&display=swap" rel="stylesheet"/>
        <style>
        .stApp {
            background-color: #0e0e0e;
            background-image: linear-gradient(to right, rgba(0, 240, 255, 0.03) 1px, transparent 1px),
                              linear-gradient(to bottom, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
            background-size: 32px 32px;
            color: #e5e2e1;
            font-family: 'Geist', sans-serif;
        }
        [data-testid="stHeader"] { display: none !important; }
        .block-container { padding-top: 2rem !important; }
        
        /* Cyber Panel styling for interactive widgets */
        [data-testid="stArrowVegaLiteChart"],
        [data-testid="stDataFrame"] {
            background-color: #1c1b1b;
            border-top: 1px solid rgba(0, 240, 255, 0.3);
            border-left: 1px solid rgba(0, 240, 255, 0.3);
            box-shadow: inset 1px 1px 0px 0px rgba(255,255,255,0.05);
            padding: 24px;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #0e0e0e; }
        ::-webkit-scrollbar-thumb { background: #3b494b; border: 1px solid #131313; }
        ::-webkit-scrollbar-thumb:hover { background: #00f0ff; }
        </style>
        """.replace('\n', ''), unsafe_allow_html=True)

        # TopAppBar
        st.markdown("""
        <header style="display: flex; justify-content: space-between; align-items: center; width: 100%; border-bottom: 1px solid rgba(59, 73, 75, 0.3); background-color: rgba(19, 19, 19, 0.8); backdrop-filter: blur(12px); padding: 16px 0; margin-top: -32px; z-index: 40; position: relative; margin-bottom: 32px; box-shadow: inset 0 0.5px 0 0 rgba(0,240,255,0.3);">
            <div style="display: flex; align-items: center;">
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: bold; color: #dbfcff; text-transform: uppercase; letter-spacing: 0.05em;">Top 5 Saham Pilihan</span>
            </div>
            <div style="display: flex; align-items: center; gap: 24px;">
                <div style="display: flex; align-items: center; gap: 16px; color: #b9cacb;">
                    <span class="material-symbols-outlined" style="cursor: pointer;">sensors</span>
                    <span class="material-symbols-outlined" style="cursor: pointer;">wifi_tethering</span>
                    <span class="material-symbols-outlined" style="cursor: pointer;">account_circle</span>
                </div>
                <button style="font-family: 'Space Mono', monospace; font-size: 11px; text-transform: uppercase; padding: 6px 16px; border: 1px solid #00f0ff; color: #00f0ff; background: transparent; cursor: pointer; letter-spacing: 0.1em; transition: all 0.3s;" onmouseover="this.style.backgroundColor='rgba(0,240,255,0.1)'" onmouseout="this.style.backgroundColor='transparent'">
                    Deploy
                </button>
            </div>
        </header>
        """.replace('\n', ''), unsafe_allow_html=True)

        # Page Header
        st.markdown("""
        <div style="margin-bottom: 32px;">
            <h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; color: #dbfcff; text-transform: uppercase; letter-spacing: 0.02em; font-weight: 600; margin-bottom: 8px;">Hasil Optimasi Portofolio</h2>
            <p style="font-family: 'Space Mono', monospace; font-size: 13px; color: #b9cacb;">Kepercayaan Model: 94.2% | Latensi: 12ms</p>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        handler = StockDataHandler([])
        df_top = handler.get_top_performers()
        
        # Generate HTML for Top 3 Performers Cards
        icons = ["military_tech", "trending_up", "show_chart"]
        cards_html = ""
        for i in range(min(3, len(df_top))):
            ticker = df_top['Ticker'].iloc[i]
            score = df_top['Skor'].iloc[i]
            risk = df_top['Risk (%)'].iloc[i]
            icon = icons[i] if i < len(icons) else "star"
            
            cards_html += f"""
            <div style="background-color: #201f1f; border: 1px solid rgba(59,73,75,0.3); padding: 20px; position: relative; overflow: hidden; box-shadow: inset 0.5px 0.5px 0 0 rgba(255,255,255,0.05); transition: all 0.3s;" onmouseover="this.style.borderColor='#00f0ff'" onmouseout="this.style.borderColor='rgba(59,73,75,0.3)'">
                <div style="position: absolute; top: 0; right: 0; padding: 12px; opacity: 0.2; color: #00f0ff;">
                    <span class="material-symbols-outlined" style="font-size: 36px;">{icon}</span>
                </div>
                <div style="position: relative; z-index: 10;">
                    <span style="font-family: 'Space Mono', monospace; font-size: 11px; color: #00f0ff; letter-spacing: 0.1em; display: block; margin-bottom: 4px;">RANK {i+1}</span>
                    <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; color: #e5e2e1; margin: 0;">{ticker}</h3>
                    <div style="margin-top: 24px; display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid rgba(59,73,75,0.2); padding-top: 16px;">
                        <div>
                            <span style="font-family: 'Space Mono', monospace; font-size: 11px; color: #b9cacb; display: block; margin-bottom: 4px;">SKOR</span>
                            <span style="font-family: 'Space Mono', monospace; font-size: 20px; color: #00f0ff; font-weight: bold;">{score}</span>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-family: 'Space Mono', monospace; font-size: 11px; color: #b9cacb; display: block; margin-bottom: 4px;">RISIKO</span>
                            <span style="font-family: 'Space Mono', monospace; font-size: 13px; color: #e5e2e1;">{risk}%</span>
                        </div>
                    </div>
                </div>
            </div>
            """
            
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 24px; margin-bottom: 32px;">
            {cards_html}
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)
        
        # Interactive Chart and DataFrame Layout
        left_col, right_col = st.columns([1, 1])
        
        with left_col:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
                <h4 style="font-family: 'Space Mono', monospace; font-size: 11px; color: #00f0ff; letter-spacing: 0.1em; text-transform: uppercase; margin: 0;">Analisis Komparasi</h4>
            </div>
            """.replace('\n', ''), unsafe_allow_html=True)
            chart_data = df_top.set_index('Ticker')[['Return (%)']]
            st.bar_chart(chart_data)
            
        with right_col:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
                <h4 style="font-family: 'Space Mono', monospace; font-size: 11px; color: #00f0ff; letter-spacing: 0.1em; text-transform: uppercase; margin: 0;">Output Sistem</h4>
            </div>
            """.replace('\n', ''), unsafe_allow_html=True)
            st.dataframe(df_top[['Ticker', 'Risk (%)', 'Skor']], hide_index=True, use_container_width=True)

if __name__ == "__main__":
    TopStocksPage().render()