import streamlit as st
import streamlit.components.v1 as components
from utils.portfolio_model import PortfolioOptimizer
from utils.sidebar import get_sidebar_html

class OptimizationPage:
    def __init__(self):
        st.set_page_config(
            page_title="Optimization",
            page_icon="⚙️",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    def render(self):
        # Inject custom sidebar
        st.markdown(get_sidebar_html("Optimize"), unsafe_allow_html=True)
        
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
        
        /* Cyber Panel styling */
        [data-testid="stHorizontalBlock"],
        [data-testid="stArrowVegaLiteChart"],
        [data-testid="stDataFrame"],
        [data-testid="stTabs"] {
            background-color: #131313;
            border-top: 1px solid rgba(0, 240, 255, 0.3);
            border-left: 1px solid rgba(0, 240, 255, 0.3);
            box-shadow: inset 1px 1px 0px 0px rgba(255,255,255,0.05);
            padding: 24px;
            margin-bottom: 24px;
            position: relative;
        }
        
        /* Inputs */
        .stTextInput input, .stNumberInput input {
            background-color: #1c1b1b !important;
            border: 1px solid #3b494b !important;
            color: #dbfcff !important;
            border-radius: 0 !important;
            font-family: 'Space Mono', monospace !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #00f0ff !important;
            box-shadow: 0 0 8px rgba(0, 240, 255, 0.4) !important;
        }
        
        /* MultiSelect */
        .stMultiSelect div[data-baseweb="select"] {
            background-color: #1c1b1b !important;
            border: 1px solid #3b494b !important;
            border-radius: 0 !important;
        }
        .stMultiSelect span[data-baseweb="tag"] {
            background-color: rgba(255, 180, 171, 0.1) !important;
            border: 1px solid rgba(255, 180, 171, 0.3) !important;
            color: #ffb4ab !important;
            border-radius: 0 !important;
            font-family: 'Space Mono', monospace !important;
        }

        /* Radio */
        .stRadio label div {
            color: #b9cacb !important;
            font-family: 'Space Mono', monospace !important;
            font-size: 13px !important;
        }

        /* Labels */
        [data-testid="stWidgetLabel"] {
            font-family: 'Space Mono', monospace !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            color: #b9cacb !important;
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
            margin-top: 28px !important;
        }
        [data-testid="stButton"] button:hover {
            background-color: rgba(0, 240, 255, 0.1) !important;
            box-shadow: 0 0 8px rgba(0, 240, 255, 0.6) !important;
            text-shadow: 0 0 4px rgba(0, 240, 255, 0.8) !important;
        }
        
        /* Metrics */
        [data-testid="metric-container"] {
            border-left: 2px solid #00f0ff;
            padding-left: 16px;
        }
        [data-testid="stMetricValue"] {
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 36px !important;
            color: #dbfcff !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricLabel"] {
            font-family: 'Space Mono', monospace !important;
            color: #b9cacb !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            font-size: 11px !important;
        }

        /* Tabs */
        button[data-baseweb="tab"] {
            font-family: 'Space Mono', monospace !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            color: #b9cacb !important;
            background-color: transparent !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #00f0ff !important;
            border-bottom-color: #00f0ff !important;
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
        <div style="margin-bottom: 32px; display: flex; justify-content: space-between; align-items: flex-end;">
            <div>
                <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 40px; color: #dbfcff; text-transform: uppercase; letter-spacing: -0.02em; font-weight: 700; margin-bottom: 8px; text-shadow: 0 0 8px rgba(0,240,255,0.3); margin-top: 0;">Dasbor Optimasi Portofolio</h1>
                <p style="font-family: 'Space Mono', monospace; font-size: 13px; color: #b9cacb; text-transform: uppercase; letter-spacing: 0.1em; margin: 0;">Sistem siap. Menunggu parameter simulasi.</p>
            </div>
            <div style="display: flex; gap: 16px;">
                <button style="font-family: 'Space Mono', monospace; font-size: 11px; text-transform: uppercase; color: #b9cacb; background: transparent; border: none; cursor: pointer; display: flex; align-items: center; gap: 8px;" onmouseover="this.style.color='#00f0ff'" onmouseout="this.style.color='#b9cacb'">
                    <span class="material-symbols-outlined" style="font-size: 18px;">download</span> Ekspor
                </button>
                <button style="font-family: 'Space Mono', monospace; font-size: 11px; text-transform: uppercase; color: #b9cacb; background: transparent; border: none; cursor: pointer; display: flex; align-items: center; gap: 8px;" onmouseover="this.style.color='#00f0ff'" onmouseout="this.style.color='#b9cacb'">
                    <span class="material-symbols-outlined" style="font-size: 18px;">share</span> Bagikan
                </button>
            </div>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        # Parameter Header
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
            <span class="material-symbols-outlined" style="color: #00f0ff; font-size: 20px;">tune</span>
            <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 18px; color: #00f0ff; text-transform: uppercase; margin: 0; letter-spacing: 0.05em;">Parameter Input</h3>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        # Filter Bar Layout
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        with col1:
            tickers = st.multiselect(
                "Pilih Saham",
                ['BBCA.JK', 'TLKM.JK', 'BMRI.JK', 'ASII.JK', 'UNVR.JK'],
                default=['BBCA.JK', 'TLKM.JK']
            )
        with col2:
            method = st.radio("Metode", ('Maximize Sharpe Ratio', 'Minimize Risk'))
        with col3:
            capital = st.number_input("Modal Awal (Rp)", min_value=1000000, value=10000000, step=1000000)
        with col4:
            run_opt = st.button("Jalankan Optimasi", type="primary", use_container_width=True)

        if run_opt:
            if not tickers:
                st.warning("Pilih minimal 1 saham untuk dioptimasi.")
                return

            optimizer = PortfolioOptimizer(tickers, capital)
            metrics = optimizer.get_kpi_metrics()
            
            # Metrics Header
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 32px; margin-bottom: 16px;">
                <span class="material-symbols-outlined" style="color: #00f0ff; font-size: 20px;">analytics</span>
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 18px; color: #00f0ff; text-transform: uppercase; margin: 0; letter-spacing: 0.05em;">Ringkasan Metrik</h3>
            </div>
            """.replace('\n', ''), unsafe_allow_html=True)
            
            # Metrics Section
            col1, col2, col3 = st.columns(3)
            col1.metric("Proyeksi Keuntungan", metrics["expected_return"])
            col2.metric("Volatilitas", metrics["volatility"])
            col3.metric("Rasio Sharpe", metrics["sharpe_ratio"])
            
            t_alloc, t_hist, t_front = st.tabs(["Alokasi", "Kinerja", "Efficient Frontier"])
            
            with t_alloc:
                st.markdown("""
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(59, 73, 75, 0.3); padding-bottom: 8px; margin-bottom: 16px;">
                    <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 18px; color: #7df4ff; text-transform: uppercase; margin: 0; letter-spacing: 0.05em;">Bobot Alokasi</h3>
                </div>
                """.replace('\n', ''), unsafe_allow_html=True)
                
                weights_df = optimizer.calculate_optimal_weights()
                st.bar_chart(weights_df.set_index('Saham'))
                
            with t_hist:
                st.write("Visualisasi Backtesting Portofolio.")
                
            with t_front:
                st.write("Visualisasi Efficient Frontier.")
                
            # Raw Data Table Header
            st.markdown("""
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(59, 73, 75, 0.3); padding-bottom: 8px; margin-top: 32px; margin-bottom: 16px;">
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 20px; color: #7df4ff; text-transform: uppercase; margin: 0; letter-spacing: 0.05em; display: flex; align-items: center; gap: 8px;">
                    <span class="material-symbols-outlined" style="font-size: 24px;">view_list</span>
                    Detail Rekomendasi
                </h3>
            </div>
            """.replace('\n', ''), unsafe_allow_html=True)
            
            report_df = optimizer.generate_allocation_report()
            
            st.dataframe(
                report_df.style.format({'Alokasi (Rp)': 'Rp {:,.0f}'}), 
                use_container_width=True, 
                hide_index=True
            )

if __name__ == "__main__":
    OptimizationPage().render()