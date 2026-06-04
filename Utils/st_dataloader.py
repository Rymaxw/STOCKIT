import streamlit as st
import os

def inisialisasi_sistem(folder_proyek: str):
    """
    Mengambil daftar saham yang sudah tersedia secara lokal di folder Data/Raw.
    Tidak lagi melakukan fetch ke yfinance untuk menghindari error koneksi.
    """
    if 'data_tersedia' not in st.session_state:
        folder_raw = os.path.join(folder_proyek, 'Data', 'Raw')
        saham_sukses = []
        
        if os.path.exists(folder_raw):
            for file in os.listdir(folder_raw):
                if file.endswith('.parquet') and not file.startswith('tickers'):
                    ticker = file.replace('.parquet', '')
                    saham_sukses.append(ticker)
                    
        # Urutkan secara alfabet
        saham_sukses.sort()
        
        st.session_state['data_tersedia'] = saham_sukses
    
    return st.session_state['data_tersedia']