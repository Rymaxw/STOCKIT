import streamlit as st
import datetime
from utils.data_handler import StockDataHandler
from utils.sidebar import get_sidebar_html

class DataExplorationPage:
    def __init__(self):
        st.set_page_config(
            page_title="Data Exploration",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    def render(self):
        # Inject custom sidebar
        st.markdown(get_sidebar_html("Data"), unsafe_allow_html=True)
        
        # Inject Custom CSS for native Streamlit widgets to match the cyber design
        st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
        <link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Space+Grotesk:wght@600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet"/>
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
        
        /* Cyber Panel styling for the filter row and chart/table containers */
        [data-testid="stHorizontalBlock"] {
            background-color: #131313;
            border-top: 1px solid rgba(0, 240, 255, 0.3);
            border-left: 1px solid rgba(0, 240, 255, 0.3);
            box-shadow: inset 1px 1px 0px 0px rgba(255,255,255,0.05);
            padding: 24px;
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
        }
        
        /* Optional glowing decorative blob in the filter bar */
        [data-testid="stHorizontalBlock"]::before {
            content: '';
            position: absolute;
            right: -40px;
            top: -40px;
            width: 160px;
            height: 160px;
            background-color: rgba(0,240,255,0.05);
            border-radius: 50%;
            filter: blur(24px);
            pointer-events: none;
        }

        [data-testid="stArrowVegaLiteChart"],
        [data-testid="stDataFrame"] {
            background-color: #131313;
            border-top: 1px solid rgba(0, 240, 255, 0.3);
            border-left: 1px solid rgba(0, 240, 255, 0.3);
            box-shadow: inset 1px 1px 0px 0px rgba(255,255,255,0.05);
            padding: 16px;
            margin-top: 16px;
        }
        
        /* Inputs */
        .stTextInput input, .stDateInput input {
            background-color: #1c1b1b !important;
            border: 1px solid #3b494b !important;
            color: #dbfcff !important;
            border-radius: 0 !important;
            font-family: 'Space Mono', monospace !important;
            padding: 12px !important;
        }
        .stTextInput input:focus, .stDateInput input:focus {
            border-color: #00f0ff !important;
            box-shadow: 0 0 8px rgba(0, 240, 255, 0.4) !important;
        }
        
        /* Labels */
        [data-testid="stWidgetLabel"] {
            font-family: 'Space Mono', monospace !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            color: #b9cacb !important;
            font-size: 11px !important;
        }
        [data-testid="stWidgetLabel"] p {
            font-size: 11px !important;
        }
        
        /* Button */
        [data-testid="stButton"] button {
            border: 1px solid #00f0ff !important;
            color: #00f0ff !important;
            background: transparent !important;
            border-radius: 0 !important;
            font-family: 'Space Mono', monospace !important;
            text-transform: uppercase !important;
            letter-spacing: 0.2em !important;
            padding: 12px 24px !important;
            height: auto !important;
            transition: all 0.2s ease-in-out !important;
            margin-top: 28px !important; /* Align with inputs */
        }
        [data-testid="stButton"] button:hover {
            background-color: rgba(0, 240, 255, 0.1) !important;
            box-shadow: 0 0 8px rgba(0, 240, 255, 0.6) !important;
            text-shadow: 0 0 4px rgba(0, 240, 255, 0.8) !important;
        }
        
        /* Custom scrollbar to match theme */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0e0e0e; 
        }
        ::-webkit-scrollbar-thumb {
            background: #3b494b; 
            border: 1px solid #131313;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #00f0ff; 
        }
        </style>
        """.replace('\n', ''), unsafe_allow_html=True)

        # TopAppBar
        st.markdown("""
        <header style="display: flex; justify-content: space-between; align-items: center; width: 100%; border-bottom: 1px solid rgba(59, 73, 75, 0.3); background-color: rgba(19, 19, 19, 0.8); backdrop-filter: blur(12px); padding: 16px 0; margin-top: -32px; z-index: 40; position: relative; margin-bottom: 32px;">
            <div style="display: flex; align-items: center; gap: 16px; color: #b9cacb; text-transform: uppercase; letter-spacing: 0.1em; font-family: 'Space Mono', monospace; font-size: 13px;">
                <span>STATUS SISTEM: <span style="color: #7df4ff;">NOMINAL</span></span>
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
            <h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 48px; color: #dbfcff; text-transform: uppercase; letter-spacing: -0.02em; font-weight: 700; margin-bottom: 8px; text-shadow: 0 0 8px rgba(0,240,255,0.3); margin-top: 0;">Eksplorasi Data Saham</h2>
            <p style="font-family: 'Space Mono', monospace; font-size: 13px; color: #b9cacb; text-transform: uppercase; letter-spacing: 0.1em; margin: 0;">QUERY // DATA_PASAR_IDX // REALTIME</p>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)
        
        # Filter Bar Layout
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            raw_tickers = st.text_input("Ticker Saham", "BBCA.JK, TLKM.JK, BMRI.JK")
            tickers = [t.strip() for t in raw_tickers.split(',')]
            
        with col2:
            today = datetime.date.today()
            one_year_ago = today - datetime.timedelta(days=365)
            date_range = st.date_input("Rentang Waktu", value=(one_year_ago, today), max_value=today)
            
        with col3:
            load_data = st.button("Muat Data", type="primary", use_container_width=True)
        
        if load_data:
            if len(date_range) != 2:
                st.error("⚠️ Pilih tanggal awal dan akhir terlebih dahulu.")
                return
                
            start_date, end_date = date_range
            
            handler = StockDataHandler(tickers)
            df_history = handler.fetch_historical_data(start_date, end_date)
            
            if not df_history.empty:
                # Chart Header
                st.markdown("""
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(59, 73, 75, 0.3); padding-bottom: 8px; margin-top: 32px;">
                    <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; color: #7df4ff; text-transform: uppercase; margin: 0; letter-spacing: 0.05em;">Pergerakan Harga Saham</h3>
                </div>
                """.replace('\n', ''), unsafe_allow_html=True)
                
                st.line_chart(df_history)
                
                # Raw Data Table Header
                st.markdown("""
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(59, 73, 75, 0.3); padding-bottom: 8px; margin-top: 32px;">
                    <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; color: #7df4ff; text-transform: uppercase; margin: 0; letter-spacing: 0.05em; display: flex; align-items: center; gap: 8px;">
                        Data Mentah
                        <span class="material-symbols-outlined" style="font-size: 20px; color: #849495; cursor: pointer;">download</span>
                    </h3>
                </div>
                """.replace('\n', ''), unsafe_allow_html=True)
                
                st.dataframe(df_history, use_container_width=True)
            else:
                st.warning("Data tidak ditemukan.")

if __name__ == "__main__":
    DataExplorationPage().render()