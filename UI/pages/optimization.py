import streamlit as st
from utils.portfolio_model import PortfolioOptimizer

class OptimizationPage:
    def render(self):
        st.title("Portfolio Optimization Dashboard")
        
        st.sidebar.header("Input Parameters")
        tickers = st.sidebar.multiselect(
            "Pilih Saham",
            ['BBCA.JK', 'TLKM.JK', 'BMRI.JK', 'ASII.JK', 'UNVR.JK'],
            default=['BBCA.JK', 'TLKM.JK']
        )
        
        method = st.sidebar.radio("Metode", ('Maximize Sharpe Ratio', 'Minimize Risk'))
        capital = st.sidebar.number_input("Modal Awal (Rp)", min_value=1000000, value=10000000, step=1000000)
        
        if st.sidebar.button("Run Optimization"):
            if not tickers:
                st.warning("Pilih minimal 1 saham untuk dioptimasi.")
                return

            optimizer = PortfolioOptimizer(tickers, capital)
            metrics = optimizer.get_kpi_metrics()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Expected Return", metrics["expected_return"])
            col2.metric("Volatility", metrics["volatility"])
            col3.metric("Sharpe Ratio", metrics["sharpe_ratio"])
            
            st.markdown("---")
            
            t_alloc, t_hist, t_front = st.tabs(["Alokasi", "Kinerja", "Efficient Frontier"])
            
            with t_alloc:
                st.subheader("Bobot Alokasi")
                weights_df = optimizer.calculate_optimal_weights()
                st.bar_chart(weights_df.set_index('Saham'))
                
            with t_hist:
                st.write("Visualisasi Backtesting Portofolio.")
                
            with t_front:
                st.write("Visualisasi Efficient Frontier.")
                
            st.markdown("---")
            st.subheader("Detail Rekomendasi")
            report_df = optimizer.generate_allocation_report()
            
            st.dataframe(
                report_df.style.format({'Alokasi (Rp)': 'Rp {:,.0f}'}), 
                use_container_width=True, 
                hide_index=True
            )

if __name__ == "__main__":
    OptimizationPage().render()