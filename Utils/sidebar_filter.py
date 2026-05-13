import streamlit as st
import pandas as pd


TICKER_BAWAAN = [
    "AAPL", "MSFT", "NVDA", "TSLA", "GOOGL",
    "AMZN", "META", "BRK-B", "JPM", "V",
    "UNH", "JNJ", "XOM", "PG", "MA",
    "HD", "CVX", "ABBV", "MRK", "LLY",
    "AVGO", "COST", "PEP", "KO", "NFLX",
    "ADBE", "CRM", "AMD", "INTC", "QCOM",
]

PETA_PERIODE = {
    "1 Bulan": "1mo",
    "3 Bulan": "3mo",
    "6 Bulan": "6mo",
    "1 Tahun": "1y",
    "21 Tahun": "21y",
}

KOLOM_URUTAN = ["Skor_Akhir", "Return_30H", "Rasio_Sharpe", "Volatilitas", "Harga"]

def render_sidebar_filter(
    tickers_default: list = None,
    period_map: dict = None,
) -> dict:
    tickers_default = tickers_default or TICKERS_DEFAULT
    period_map      = period_map or PERIOD_MAP

    with st.sidebar:
        st.markdown("##Panel Filter")
        st.markdown("---")

            st.markdown("**Periode Data**")
            periode_terpilih = st.selectbox(
                label="Pilih periode",
                options=list(self.peta_periode.keys()),
                index=3,
                label_visibility="collapsed",
                key="sf_periode",
            )
            kode_periode_yf = self.peta_periode[periode_terpilih]

            st.markdown("---")

            st.markdown("**Pilih Saham**")
            daftar_terpilih = st.multiselect(
                label="Ticker yang ditampilkan",
                options=self.daftar_ticker,
                default=self.daftar_ticker[:10],
                label_visibility="collapsed",
                key="sf_tickers",
            )
            if not daftar_terpilih:
                st.warning("Pilih minimal 1 saham.")
                daftar_terpilih = self.daftar_ticker[:5]

            st.markdown("---")

            st.markdown("**Urutkan Berdasarkan**")
            kolom_urut = st.selectbox(
                label="Kolom urutan",
                options=KOLOM_URUTAN,
                label_visibility="collapsed",
                key="sf_kolom_urut",
            )
            pilihan_urutan = st.radio(
                label="Urutan",
                options=["⬆ Tertinggi → Terendah", "⬇ Terendah → Tertinggi"],
                index=0,
                label_visibility="collapsed",
                key="sf_urutan",
            )
            urut_naik = pilihan_urutan == "⬇ Terendah → Tertinggi"

            st.markdown("---")

            st.markdown("**Filter Metrik**")

            min_return = st.slider(
                label="Min Return 30H (%)",
                min_value=-50,
                max_value=100,
                value=-50,
                step=1,
                key="sf_min_return",
            ) / 100

            maks_volatilitas = st.slider(
                label="Maks Volatilitas (%/tahun)",
                min_value=0,
                max_value=200,
                value=200,
                step=5,
                key="sf_maks_vol",
            ) / 100

            min_sharpe = st.slider(
                label="Min Sharpe Ratio",
                min_value=-5.0,
                max_value=5.0,
                value=-5.0,
                step=0.1,
                key="sf_min_sharpe",
            )

            st.markdown("---")

            st.markdown("**Tampilkan Top N**")
            jumlah_tampil = st.slider(
                label="Jumlah baris",
                min_value=3,
                max_value=max(len(daftar_terpilih), 3),
                value=min(10, len(daftar_terpilih)),
                label_visibility="collapsed",
                key="sf_jumlah_tampil",
            )

            st.markdown("---")
            st.markdown(
                "<small style='color:#8b949e'>"
                "Data dari Yahoo Finance.<br>"
                "Jika offline, pakai data sintetis."
                "</small>",
                unsafe_allow_html=True,
            )

        return {
            "daftar_ticker":   daftar_terpilih,
            "periode_ui":      periode_terpilih,
            "kode_periode_yf": kode_periode_yf,
            "kolom_urut":      kolom_urut,
            "urut_naik":       urut_naik,
            "min_return":      min_return,
            "maks_volatilitas": maks_volatilitas,
            "min_sharpe":      min_sharpe,
            "jumlah_tampil":   jumlah_tampil,
        }


class ProsesFilter:

    @staticmethod
    def terapkan(df_peringkat: pd.DataFrame, filter_aktif: dict) -> pd.DataFrame:
        if df_peringkat.empty:
            return df_peringkat

        df = df_peringkat.copy()

        masker = (
            (df["Return_30H"]   >= filter_aktif["min_return"])    &
            (df["Volatilitas"]  <= filter_aktif["maks_volatilitas"]) &
            (df["Rasio_Sharpe"] >= filter_aktif["min_sharpe"])
        )
        df = df[masker]

        kolom_urut = filter_aktif["kolom_urut"]
        if kolom_urut in df.columns:
            df = df.sort_values(kolom_urut, ascending=filter_aktif["urut_naik"])

        return df.head(filter_aktif["jumlah_tampil"])

    @staticmethod
    def format_tabel(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        df_tampil = df.copy()
        df_tampil["Return_30H"]   = df_tampil["Return_30H"].apply(lambda x: f"{x:+.2%}")
        df_tampil["Rasio_Sharpe"] = df_tampil["Rasio_Sharpe"].apply(lambda x: f"{x:.3f}")
        df_tampil["Volatilitas"]  = df_tampil["Volatilitas"].apply(lambda x: f"{x:.2%}")
        df_tampil["Harga"]        = df_tampil["Harga"].apply(lambda x: f"${x:,.2f}")
        df_tampil["Skor_Akhir"]   = df_tampil["Skor_Akhir"].apply(lambda x: f"{x:.4f}")
        return df_tampil