import streamlit as st
from utils.data_handler import StockDataHandler

class TopStocksPage:
    def render(self):
        st.title("Top 5 Saham Pilihan")
        st.divider()
        
        handler = StockDataHandler([])
        df_top = handler.get_top_performers()
        
        st.subheader("Top 3 Performers")
        cols = st.columns(3)
        
        for i in range(3):
            with cols[i]:
                st.metric(
                    label=f"Rank {i+1}: {df_top['Ticker'][i]}", 
                    value=f"{df_top['Return (%)'][i]}%",
                    delta=f"Risk: {df_top['Risk (%)'][i]}%",
                    delta_color="off"
                )
                
        st.write("")
        st.subheader("Analisis Komparasi")
        left_col, right_col = st.columns([2, 1])
        
        with left_col:
            chart_data = df_top.set_index('Ticker')[['Return (%)']]
            st.bar_chart(chart_data)
            
        with right_col:
            st.dataframe(df_top[['Ticker', 'Risk (%)', 'Skor']], hide_index=True, use_container_width=True)

if __name__ == "__main__":
    TopStocksPage().render()