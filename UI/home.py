import streamlit as st
import streamlit.components.v1 as components
import os
from utils.sidebar import get_sidebar_html
from Utils.st_dataloader import inisialisasi_sistem

class HomePage:
    def __init__(self):
        st.set_page_config(
            page_title="STOCKIT - Stock Portfolio",
            page_icon="🏠",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        folder_utama = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        inisialisasi_sistem(folder_utama)

    def render(self):
        # Hide default Streamlit elements to make the custom HTML full-screen
        hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
            }
            </style>
            """
        st.markdown(hide_st_style, unsafe_allow_html=True)

        # Inject the native Streamlit DOM sidebar
        st.markdown(get_sidebar_html("Home"), unsafe_allow_html=True)

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

        /* Custom buttons styling to match cyber theme */
        [data-testid="stButton"] button {
            border: 1px solid #00f0ff !important;
            color: #00f0ff !important;
            background: transparent !important;
            border-radius: 0 !important;
            font-family: 'Space Mono', monospace !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            padding: 16px 24px !important;
            height: auto !important;
            transition: all 0.2s ease-in-out !important;
            box-shadow: inset 0 0 10px rgba(0,240,255,0.1) !important;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        [data-testid="stButton"] button:hover {
            background-color: rgba(0, 240, 255, 0.1) !important;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.4), inset 0 0 10px rgba(0,240,255,0.2) !important;
            text-shadow: 0 0 4px rgba(0, 240, 255, 0.8) !important;
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
            <div style="display: flex; align-items: center; gap: 8px; font-family: 'Space Mono', monospace; font-size: 13px;">
                <span style="color: #b9cacb;">SYS</span>
                <span style="color: #00f0ff;">/</span>
                <span style="color: #00f0ff; font-weight: bold;">HOME</span>
            </div>
            <div style="display: flex; align-items: center; gap: 24px;">
                <div style="display: flex; align-items: center; gap: 16px; color: #00f0ff;">
                    <span class="material-symbols-outlined" style="cursor: pointer;">sensors</span>
                    <span class="material-symbols-outlined" style="cursor: pointer;">wifi_tethering</span>
                    <span class="material-symbols-outlined" style="cursor: pointer;">account_circle</span>
                </div>
                <button style="font-family: 'Space Mono', monospace; font-size: 11px; text-transform: uppercase; padding: 6px 16px; border: 1px solid #3b494b; color: #e5e2e1; background: #1c1b1b; cursor: pointer; letter-spacing: 0.1em; transition: all 0.3s; display: flex; items-center; gap: 8px;" onmouseover="this.style.borderColor='#00f0ff'; this.style.color='#00f0ff'" onmouseout="this.style.borderColor='#3b494b'; this.style.color='#e5e2e1'">
                    <span class="material-symbols-outlined" style="font-size: 14px;">cloud_upload</span> Deploy
                </button>
            </div>
        </header>
        """.replace('\n', ''), unsafe_allow_html=True)

        # Hero Section
        st.markdown("""
        <div style="margin-bottom: 48px; border-left: 4px solid #00f0ff; padding-left: 24px;">
            <h2 style="font-family: 'Space Grotesk', sans-serif; font-size: 48px; color: #e5e2e1; margin-bottom: 8px; display: flex; align-items: center; gap: 16px;">
                STOCKIT 
                <span class="material-symbols-outlined" style="color: #00f0ff; font-size: 48px; font-variation-settings: 'FILL' 1;">dataset</span>
            </h2>
            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; color: #b9cacb; margin: 0; padding-top: 8px;">
                Data Science App for Stock Portfolio Optimization
            </p>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        with col1:
            # Quick Start Box replacing the non-functional parameter input
            st.markdown("""
            <div style="background-color: rgba(42, 42, 42, 0.4); border: 1px solid rgba(0, 240, 255, 0.5); padding: 24px; margin-bottom: 24px; position: relative; box-shadow: 0 0 15px rgba(0,240,255,0.05); transition: all 0.3s;" onmouseover="this.style.borderColor='#00f0ff'" onmouseout="this.style.borderColor='rgba(0, 240, 255, 0.5)'">
                <div style="display: flex; align-items: center; gap: 12px; border-bottom: 1px solid rgba(59, 73, 75, 0.3); padding-bottom: 16px; margin-bottom: 16px;">
                    <span class="material-symbols-outlined" style="color: #00f0ff;">rocket_launch</span>
                    <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; color: #e5e2e1; text-transform: uppercase; margin: 0; letter-spacing: 0.05em;">Mulai Cepat</h3>
                </div>
                <p style="font-family: 'Geist', sans-serif; font-size: 14px; color: #b9cacb; margin-bottom: 24px; line-height: 1.6;">
                    Aplikasi ini membantu merancang portofolio saham menggunakan pendekatan kuantitatif modern. 
                    Klik tombol di bawah untuk masuk ke dasbor optimasi dan mengatur parameter simulasi Anda.
                </p>
            </div>
            """.replace('\n', ''), unsafe_allow_html=True)
            
            if st.button("Buka Dasbor Optimasi", use_container_width=True):
                st.switch_page("pages/optimization.py")

            # System Status Block
            st.markdown("""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 24px;">
                <div style="background-color: #201f1f; border: 1px solid rgba(59, 73, 75, 0.2); padding: 16px; display: flex; flex-direction: column; gap: 8px;">
                    <span style="font-family: 'Space Mono', monospace; font-size: 11px; color: #b9cacb; text-transform: uppercase;">Status Mesin</span>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 8px; height: 8px; background-color: #00f0ff; border-radius: 50%; box-shadow: 0 0 8px #00f0ff;"></div>
                        <span style="font-family: 'Space Mono', monospace; font-size: 13px; color: #00f0ff;">ONLINE</span>
                    </div>
                </div>
                <div style="background-color: #201f1f; border: 1px solid rgba(59, 73, 75, 0.2); padding: 16px; display: flex; flex-direction: column; gap: 8px;">
                    <span style="font-family: 'Space Mono', monospace; font-size: 11px; color: #b9cacb; text-transform: uppercase;">Data Feed</span>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span class="material-symbols-outlined" style="font-size: 16px; color: #849495;">sync</span>
                        <span style="font-family: 'Space Mono', monospace; font-size: 13px; color: #e5e2e1;">SINKRON</span>
                    </div>
                </div>
            </div>
            """.replace('\n', ''), unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background-color: #201f1f; border: 1px solid rgba(0, 240, 255, 0.8); padding: 32px 24px; text-align: center; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(0,240,255,0.15); cursor: pointer; transition: all 0.3s;" onmouseover="this.style.boxShadow='0 0 30px rgba(0,240,255,0.3)'; this.style.backgroundColor='rgba(0,240,255,0.05)'" onmouseout="this.style.boxShadow='0 0 20px rgba(0,240,255,0.15)'; this.style.backgroundColor='#201f1f'">
                <span class="material-symbols-outlined" style="font-size: 64px; color: #00f0ff; margin-bottom: 24px; text-shadow: 0 0 12px rgba(0,240,255,0.8);">query_stats</span>
                <p style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; color: #00f0ff; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 32px;">Eksplorasi Data</p>
                <div style="display: flex; gap: 8px;">
                    <div style="width: 6px; height: 6px; background-color: rgba(0,240,255,0.4); border-radius: 50%;"></div>
                    <div style="width: 6px; height: 6px; background-color: rgba(0,240,255,0.6); border-radius: 50%;"></div>
                    <div style="width: 6px; height: 6px; background-color: #00f0ff; border-radius: 50%; box-shadow: 0 0 8px #00f0ff;"></div>
                </div>
            </div>
            """.replace('\n', ''), unsafe_allow_html=True)
            
            # Invisible button over the box to make it clickable
            if st.button("Eksplorasi Market Data Sekarang", use_container_width=True):
                st.switch_page("pages/data_exploration.py")

if __name__ == "__main__":
    app = HomePage()
    app.render()