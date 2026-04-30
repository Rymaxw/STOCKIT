import streamlit as st
import datetime
from utils.data_handler import StockDataHandler

class DataExplorationPage:
    def render(self):
        st.title("Stock Data Exploration")
        
        st.sidebar.header("Filter Data")
        raw_tickers = st.sidebar.text_input("Ticker Saham", "BBCA.JK, TLKM.JK, BMRI.JK")
        tickers = raw_tickers.split(',')
        
        # Setup default tanggal (1 tahun ke belakang)
        today = datetime.date.today()
        one_year_ago = today - datetime.timedelta(days=365)
        
        date_range = st.sidebar.date_input(
            "Rentang Waktu",
            value=(one_year_ago, today),
            max_value=today
        )
        
        if st.sidebar.button("Load Data"):
            # Validasi input tanggal harus milih rentang yang lengkap
            if len(date_range) != 2:
                st.sidebar.error("⚠️ Pilih tanggal awal dan akhir terlebih dahulu.")
                return
                
            start_date, end_date = date_range
            
            handler = StockDataHandler(tickers)
            df_history = handler.fetch_historical_data(start_date, end_date)
            
            if not df_history.empty:
                st.subheader("Pergerakan Harga Saham")
                st.line_chart(df_history) # Sumbu X otomatis jadi tanggal karena pake index pd.date_range
                
                st.subheader("Raw Data")
                st.dataframe(df_history, use_container_width=True)
            else:
                st.warning("Data tidak ditemukan.")

if __name__ == "__main__":
    DataExplorationPage().render()