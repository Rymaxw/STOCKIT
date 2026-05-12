import streamlit as st
import pandas as pd

TICKERS_DEFAULT = [
    "AAPL", "MSFT", "NVDA", "TSLA", "GOOGL",
    "AMZN", "META", "BRK-B", "JPM", "V",
    "UNH", "JNJ", "XOM", "PG", "MA",
    "HD", "CVX", "ABBV", "MRK", "LLY",
    "AVGO", "COST", "PEP", "KO", "NFLX",
    "ADBE", "CRM", "AMD", "INTC", "QCOM",
]

PERIOD_MAP = {
    "1 Bulan": "1mo",
    "3 Bulan": "3mo",
    "6 Bulan": "6mo",
    "1 Tahun": "1y",
    "2 Tahun": "2y",
}

SORT_COLUMNS = ["Final Score", "Return 30D", "Sharpe", "Volatilitas", "Harga"]

def render_sidebar_filter(
    tickers_default: list = None,
    period_map: dict = None,
) -> dict:
    tickers_default = tickers_default or TICKERS_DEFAULT
    period_map      = period_map or PERIOD_MAP

    with st.sidebar:
        st.markdown("## Panel Filter")
        st.markdown("---")

        st.markdown("**Periode Data**")
        periode_ui = st.selectbox(
            label="Pilih periode",
            options=list(period_map.keys()),
            index=3,
            label_visibility="collapsed",
            key="sf_periode",
        )
        periode_yf = period_map[periode_ui]

        st.markdown("---")

        st.markdown("**Pilih Saham**")
        selected_tickers = st.multiselect(
            label="Ticker yang ditampilkan",
            options=tickers_default,
            default=tickers_default[:10],
            label_visibility="collapsed",
            key="sf_tickers",
        )
        if not selected_tickers:
            st.warning("Pilih minimal 1 saham.")
            selected_tickers = tickers_default[:5]

        st.markdown("---")

        st.markdown("**Urutkan Berdasarkan**")
        sort_col = st.selectbox(
            label="Kolom sort",
            options=SORT_COLUMNS,
            label_visibility="collapsed",
            key="sf_sort_col",
        )
        sort_order = st.radio(
            label="Urutan",
            options=["⬆ Tertinggi → Terendah", "⬇ Terendah → Tertinggi"],
            index=0,
            label_visibility="collapsed",
            key="sf_sort_order",
        )
        sort_ascending = sort_order == "⬇ Terendah → Tertinggi"

        st.markdown("---")

        st.markdown("**Filter Metrik**")

        min_return = st.slider(
            label="Min Return 30D (%)",
            min_value=-50,
            max_value=100,
            value=-50,
            step=1,
            key="sf_min_return",
        ) / 100   # Konversi ke desimal

        max_volatility = st.slider(
            label="Max Volatilitas (%/tahun)",
            min_value=0,
            max_value=200,
            value=200,
            step=5,
            key="sf_max_vol",
        ) / 100   # Konversi ke desimal

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
        top_n = st.slider(
            label="Jumlah baris",
            min_value=3,
            max_value=max(len(selected_tickers), 3),
            value=min(10, len(selected_tickers)),
            label_visibility="collapsed",
            key="sf_top_n",
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
        "tickers":        selected_tickers,
        "periode_ui":     periode_ui,
        "periode_yf":     periode_yf,
        "sort_col":       sort_col,
        "sort_ascending": sort_ascending,
        "min_return":     min_return,
        "max_volatility": max_volatility,
        "min_sharpe":     min_sharpe,
        "top_n":          top_n,
    }

def apply_filters(df_ranking: pd.DataFrame, filters: dict) -> pd.DataFrame:
    if df_ranking.empty:
        return df_ranking

    df = df_ranking.copy()

    mask = (
        (df["Return 30D"]  >= filters["min_return"])    &
        (df["Volatilitas"] <= filters["max_volatility"]) &
        (df["Sharpe"]      >= filters["min_sharpe"])
    )
    df = df[mask]

    sort_col = filters["sort_col"]
    if sort_col in df.columns:
        df = df.sort_values(sort_col, ascending=filters["sort_ascending"])

    df = df.head(filters["top_n"])

    return df

def format_ranking_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    df_fmt = df.copy()
    df_fmt["Return 30D"]  = df_fmt["Return 30D"].apply(lambda x: f"{x:+.2%}")
    df_fmt["Sharpe"]      = df_fmt["Sharpe"].apply(lambda x: f"{x:.3f}")
    df_fmt["Volatilitas"] = df_fmt["Volatilitas"].apply(lambda x: f"{x:.2%}")
    df_fmt["Harga"]       = df_fmt["Harga"].apply(lambda x: f"${x:,.2f}")
    df_fmt["Final Score"] = df_fmt["Final Score"].apply(lambda x: f"{x:.4f}")
    return df_fmt