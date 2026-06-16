import streamlit as st
import os
import json
from Utils.data_pipeline import OrkestratorPipeline, PengambilDataSaham, PemrosesData, ManajerPenyimpanan

def baca_daftar_ticker(lokasi_json: str) -> list:
    with open(lokasi_json, 'r') as berkas:
        data_json = json.load(berkas)
        daftar_saham = [item['yf_symbol'] for item in data_json['tickers']]
    return daftar_saham

@st.cache_data(ttl=3600, show_spinner="Sinkronisasi data...")
def tarik_data_dengan_cache(daftar_saham: list, folder_proyek: str) -> list:
    pipeline = OrkestratorPipeline(
        PengambilDataSaham(),
        PemrosesData(),
        ManajerPenyimpanan(folder_proyek)
    )
    sukses, gagal = pipeline.jalankan_paralel(daftar_saham)
    return sukses

def inisialisasi_sistem(folder_proyek: str):
    if 'data_tersedia' not in st.session_state:
        lokasi_json = os.path.join(folder_proyek, 'Data', 'Raw', 'tickers_us.json')
        daftar_saham = baca_daftar_ticker(lokasi_json)
        
        saham_sukses = []
        if daftar_saham:
            saham_sukses = tarik_data_dengan_cache(daftar_saham, folder_proyek)
            
        if not saham_sukses:
            folder_raw = os.path.join(folder_proyek, 'Data', 'Raw')
            if os.path.exists(folder_raw):
                for file in os.listdir(folder_raw):
                    if file.endswith('.parquet') and not file.startswith('tickers'):
                        ticker = file.replace('.parquet', '')
                        if ticker not in saham_sukses:
                            saham_sukses.append(ticker)
        
        saham_sukses.sort()
        st.session_state['data_tersedia'] = saham_sukses
        
    return st.session_state['data_tersedia']