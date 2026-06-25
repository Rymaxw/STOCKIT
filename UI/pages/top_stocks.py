import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from UI.utils.data_handler import PengelolaDataSahamUI
from UI.utils.sidebar import dapatkan_html_sidebar


class HalamanSahamTerbaik:

    def __init__(self):
        st.set_page_config(
            page_title="Top Stocks — STOCKIT",
            page_icon="⭐",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    # ── Global Styles ────────────────────────────────────────────────
    def _suntik_gaya(self):
        st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>', unsafe_allow_html=True)
        st.markdown('<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"/>', unsafe_allow_html=True)

        st.markdown("""<style>
        .stApp {
            background-color: #0c0e17;
            color: #e2e1f0;
            font-family: 'Space Grotesk', sans-serif;
        }
        .stApp::before {
            content: '';
            position: fixed;
            top: -10%;
            left: -5%;
            width: 40vw;
            height: 40vw;
            background: rgba(164,230,255,0.05);
            filter: blur(100px);
            border-radius: 50%;
            z-index: -1;
            pointer-events: none;
        }
        .stApp::after {
            content: '';
            position: fixed;
            bottom: -20%;
            right: -10%;
            width: 50vw;
            height: 50vw;
            background: rgba(49,49,192,0.05);
            filter: blur(120px);
            border-radius: 50%;
            z-index: -1;
            pointer-events: none;
        }
        [data-testid="stHeader"] { display: none !important }
        .block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
        [data-testid="stExpander"] {
            background: rgba(255,255,255,0.03);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 0.5px solid rgba(255,255,255,0.1);
            border-radius: 0.75rem;
        }
        [data-testid="stExpander"] summary span {
            font-family: 'Space Grotesk', sans-serif !important;
            color: #e2e1f0 !important;
            font-weight: 500 !important;
        }
        ::-webkit-scrollbar { width: 4px; height: 4px }
        ::-webkit-scrollbar-track { background: transparent }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2) }
        /* Hide default streamlit area chart backgrounds */
        [data-testid="stArrowVegaLiteChart"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }
        </style>""", unsafe_allow_html=True)

    # ── Main Render ──────────────────────────────────────────────────
    def render(self):
        st.markdown(dapatkan_html_sidebar("Top Stocks"), unsafe_allow_html=True)
        self._suntik_gaya()

        self._render_header_halaman()
        self._render_konten_utama()

    # ── Header ───────────────────────────────────────────────────────
    def _render_header_halaman(self):
        st.markdown("""
        <div style="margin-bottom: 40px; display: flex; justify-content: space-between; align-items: flex-end;">
            <div style="display: flex; flex-direction: column; gap: 12px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 6px; height: 36px; background: linear-gradient(180deg, #a4e6ff, #3131c0); border-radius: 9999px; box-shadow: 0 0 12px rgba(164,230,255,0.6);"></div>
                    <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 48px; color: #e2e1f0; font-weight: 600; line-height: 1.1; letter-spacing: -0.02em; margin: 0; text-shadow: 0 0 20px rgba(164,230,255,0.4);">Top 5 Saham Pilihan</h1>
                </div>
                <p style="font-family: 'Space Grotesk', sans-serif; font-size: 15px; color: #8a9aa0; max-width: 48rem; margin: 0; line-height: 1.6; letter-spacing: 0.01em;">
                    Ranking otomatis berdasarkan <strong style="color: #bbc9cf;">Return 30 Hari (40%)</strong>, <strong style="color: #bbc9cf;">Sharpe Ratio (40%)</strong>, dan <strong style="color: #bbc9cf;">Volatilitas Rendah (20%)</strong>. Data live dari Yahoo Finance.
                </p>
            </div>
            <div style="display: flex; gap: 12px; flex-shrink: 0;">
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 600; color: #a4e7f6; display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.04); backdrop-filter: blur(12px); border: 0.5px solid rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.08em;">
                    <span style="width: 8px; height: 8px; background-color: #4cd6ff; border-radius: 50%; box-shadow: 0 0 8px #4cd6ff; animation: pulse 2s infinite;"></span>
                    Live Data
                </span>
            </div>
        </div>
        <style>@keyframes pulse { 0% { opacity: 1 } 50% { opacity: 0.4 } 100% { opacity: 1 } }</style>
        """.replace('\n', ''), unsafe_allow_html=True)

    # ── Main Content ─────────────────────────────────────────────────
    def _render_konten_utama(self):
        pengelola = PengelolaDataSahamUI([])

        with st.spinner("Mengunduh data live dari Yahoo Finance..."):
            hasil = pengelola.ambil_saham_terbaik_live()

        df_terbaik = hasil.get('tabel', pd.DataFrame())
        df_historis = hasil.get('historis', pd.DataFrame())
        df_ohlcv = hasil.get('ohlcv', pd.DataFrame())

        if df_terbaik.empty:
            st.warning("Gagal mengunduh data live saham dari Yahoo Finance. Silakan periksa koneksi internet Anda.")
            return

        st.markdown('<div style="margin-bottom: 24px;"></div>', unsafe_allow_html=True)

        self._render_kartu_top5(df_terbaik, df_historis)

        st.markdown('<div style="margin-top: 48px;"></div>', unsafe_allow_html=True)

        self._render_analisis_section(df_terbaik, df_historis, df_ohlcv)

    # ── Top 5 Cards with Sparklines ──────────────────────────────────
    def _render_kartu_top5(self, df_terbaik, df_historis):
        jumlah_tampil = min(5, len(df_terbaik))
        kolom_list = st.columns(jumlah_tampil)

        for i in range(jumlah_tampil):
            with kolom_list[i]:
                row = df_terbaik.iloc[i]
                ticker = row['Ticker']
                skor = row['Skor']
                risiko = row['Risiko (%)']
                ret_30d = row['Return (%)']
                harga = row.get('Harga', 0)
                perubahan = row.get('Perubahan Harian (%)', 0)

                rank = i + 1

                # Warna perubahan harian
                warna_harian = "#4ade80" if perubahan >= 0 else "#f87171"
                ikon_harian = "arrow_upward" if perubahan >= 0 else "arrow_downward"

                # Warna return 30 hari
                warna_ret = "#4ade80" if ret_30d >= 0 else "#f87171"

                # Badge rank colors
                if rank == 1:
                    rank_bg = "linear-gradient(135deg, rgba(255,215,0,0.25), rgba(255,180,0,0.1))"
                    rank_border = "rgba(255,215,0,0.5)"
                    rank_color = "#ffd700"
                    rank_emoji = "🥇"
                elif rank == 2:
                    rank_bg = "linear-gradient(135deg, rgba(192,192,192,0.25), rgba(160,160,160,0.1))"
                    rank_border = "rgba(192,192,192,0.5)"
                    rank_color = "#c0c0c0"
                    rank_emoji = "🥈"
                elif rank == 3:
                    rank_bg = "linear-gradient(135deg, rgba(205,127,50,0.25), rgba(180,100,30,0.1))"
                    rank_border = "rgba(205,127,50,0.5)"
                    rank_color = "#cd7f32"
                    rank_emoji = "🥉"
                else:
                    rank_bg = "rgba(164,230,255,0.1)"
                    rank_border = "rgba(164,230,255,0.3)"
                    rank_color = "#a4e6ff"
                    rank_emoji = f"#{rank}"

                st.markdown(f"""
                <div style="background: linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(16,0,169,0.04) 100%); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 0.5px solid rgba(255,255,255,0.08); border-top-color: rgba(255,255,255,0.15); border-left-color: rgba(255,255,255,0.15); padding: 24px 20px; border-radius: 12px; position: relative; overflow: hidden; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-4px)'; this.style.borderColor='rgba(164,230,255,0.3)'; this.style.boxShadow='0 12px 40px rgba(0,209,255,0.08)'" onmouseout="this.style.transform='translateY(0)'; this.style.borderColor='rgba(255,255,255,0.08)'; this.style.boxShadow='none'">
                    <div style="position: absolute; top: -30px; right: -30px; width: 100px; height: 100px; background: rgba(164,230,255,0.15); border-radius: 50%; filter: blur(35px); z-index: 0;"></div>
                    <div style="position: relative; z-index: 10;">
                        <!-- Rank & Ticker -->
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <span style="width: 28px; height: 28px; border-radius: 50%; background: {rank_bg}; border: 1px solid {rank_border}; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: {rank_color};">{rank_emoji}</span>
                                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 600; color: #e2e1f0; letter-spacing: -0.01em;">{ticker}</span>
                            </div>
                        </div>

                        <!-- Price -->
                        <div style="margin-bottom: 6px;">
                            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 600; color: #ffffff; letter-spacing: -0.02em;">${harga:,.2f}</span>
                        </div>

                        <!-- Daily Change Badge -->
                        <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 20px;">
                            <div style="display: inline-flex; align-items: center; gap: 3px; background: {'rgba(74,222,128,0.1)' if perubahan >= 0 else 'rgba(248,113,113,0.1)'}; padding: 3px 10px; border-radius: 9999px; border: 1px solid {'rgba(74,222,128,0.2)' if perubahan >= 0 else 'rgba(248,113,113,0.2)'};">
                                <span class="material-symbols-outlined" style="font-size: 14px; color: {warna_harian};">{ikon_harian}</span>
                                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 600; color: {warna_harian};">{perubahan:+.2f}%</span>
                            </div>
                            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 10px; color: #6b7b82;">today</span>
                        </div>

                        <!-- 30D Return -->
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding: 10px 12px; background: rgba(255,255,255,0.03); border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 10px; font-weight: 600; color: #8a9aa0; text-transform: uppercase; letter-spacing: 0.06em;">Return 30D</span>
                            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; font-weight: 600; color: {warna_ret};">{ret_30d:+.2f}%</span>
                        </div>

                        <!-- Composite Score -->
                        <div style="margin-bottom: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 10px; font-weight: 600; color: #8a9aa0; text-transform: uppercase; letter-spacing: 0.06em;">Composite Score</span>
                                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 14px; font-weight: 600; color: #a4e6ff; text-shadow: 0 0 8px rgba(164,230,255,0.5);">{skor}<span style="font-size: 10px; color: rgba(164,230,255,0.6);">/100</span></span>
                            </div>
                            <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.08); border-radius: 9999px; overflow: hidden;">
                                <div style="height: 100%; background: linear-gradient(90deg, #3131c0, #a4e6ff); width: {skor}%; border-radius: 9999px; box-shadow: 0 0 8px rgba(164,230,255,0.6);"></div>
                            </div>
                        </div>

                        <!-- Risk -->
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 10px; font-weight: 600; color: #8a9aa0; text-transform: uppercase; letter-spacing: 0.06em;">Risk</span>
                            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 500; color: #bbc9cf;">{risiko}%</span>
                        </div>
                    </div>
                </div>
                """.replace('\n', ''), unsafe_allow_html=True)

    # ── Analysis Section: Scatter Plot + Candlestick ─────────────────
    def _render_analisis_section(self, df_terbaik, df_historis, df_ohlcv):
        kolom_kiri, kolom_kanan = st.columns([1, 1])

        with kolom_kiri:
            self._render_scatter_plot(df_terbaik)

        with kolom_kanan:
            self._render_tabel_data(df_terbaik)

        st.markdown('<div style="margin-top: 32px;"></div>', unsafe_allow_html=True)
        self._render_candlestick_expander(df_terbaik, df_ohlcv)

    # ── Risk vs Return Scatter Plot ──────────────────────────────────
    def _render_scatter_plot(self, df_terbaik):
        st.markdown("""
        <div style="margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span class="material-symbols-outlined" style="font-size: 22px; color: #a4e6ff;">scatter_plot</span>
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Risk-Return Profile</h3>
            </div>
            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 13px; color: #6b7b82; margin: 0;">Semakin kanan atas, semakin tinggi return namun risiko juga besar. Ukuran titik mencerminkan Composite Score.</p>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        top5 = df_terbaik.head(5)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=top5['Risiko (%)'],
            y=top5['Return (%)'],
            mode='markers+text',
            marker=dict(
                size=top5['Skor'] / 2.5,
                color=top5['Skor'],
                colorscale=[[0, '#3131c0'], [0.5, '#a4e6ff'], [1, '#4ade80']],
                showscale=True,
                colorbar=dict(
                    title=dict(text='Score', font=dict(color='#bbc9cf', family='Space Grotesk', size=11)),
                    tickfont=dict(color='#8a9aa0', family='Space Grotesk', size=10),
                    bgcolor='rgba(0,0,0,0)',
                    borderwidth=0,
                    len=0.6,
                ),
                line=dict(width=1, color='rgba(255,255,255,0.3)'),
                opacity=0.9,
            ),
            text=top5['Ticker'],
            textposition='top center',
            textfont=dict(color='#e2e1f0', family='Space Grotesk', size=12),
            hovertemplate=(
                '<b>%{text}</b><br>'
                'Risk: %{x:.2f}%<br>'
                'Return 30D: %{y:.2f}%<br>'
                'Score: %{marker.color:.1f}<extra></extra>'
            ),
        ))

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk', color='#bbc9cf'),
            xaxis=dict(
                title='Volatilitas / Risiko (%)',
                gridcolor='rgba(255,255,255,0.05)',
                zerolinecolor='rgba(255,255,255,0.1)',
                tickfont=dict(size=11),
            ),
            yaxis=dict(
                title='Return 30 Hari (%)',
                gridcolor='rgba(255,255,255,0.05)',
                zerolinecolor='rgba(255,255,255,0.1)',
                tickfont=dict(size=11),
            ),
            margin=dict(l=40, r=20, t=20, b=40),
            height=380,
            showlegend=False,
        )

        st.plotly_chart(fig, width="stretch")

    # ── Data Table ───────────────────────────────────────────────────
    def _render_tabel_data(self, df_terbaik):
        st.markdown("""
        <div style="margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <span class="material-symbols-outlined" style="font-size: 22px; color: #a4e6ff;">table_chart</span>
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Data Output</h3>
            </div>
            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 13px; color: #6b7b82; margin: 0;">Tabel lengkap metrik evaluasi saham terbaik.</p>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        # Pilih kolom yang relevan untuk ditampilkan
        kolom_tampil = ['Ticker', 'Harga', 'Perubahan Harian (%)', 'Return (%)', 'Risiko (%)', 'Skor']
        kolom_ada = [k for k in kolom_tampil if k in df_terbaik.columns]

        st.dataframe(
            df_terbaik[kolom_ada],
            hide_index=True,
            width="stretch",
        )

    # ── Interactive Candlestick Expander ──────────────────────────────
    def _render_candlestick_expander(self, df_terbaik, df_ohlcv):
        top5_tickers = df_terbaik['Ticker'].head(5).tolist()

        st.markdown("""
        <div style="margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span class="material-symbols-outlined" style="font-size: 22px; color: #a4e6ff;">candlestick_chart</span>
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 500; color: #e2e1f0; letter-spacing: -0.01em; margin: 0;">Analisis Teknikal</h3>
            </div>
            <p style="font-family: 'Space Grotesk', sans-serif; font-size: 13px; color: #6b7b82; margin: 4px 0 0 0;">Pilih salah satu saham dari Top 5 untuk melihat grafik Candlestick interaktif (60 hari) dengan SMA 20.</p>
        </div>
        """.replace('\n', ''), unsafe_allow_html=True)

        selected_ticker = st.selectbox(
            "Pilih Saham",
            top5_tickers,
            index=0,
            label_visibility="collapsed",
        )

        if df_ohlcv.empty:
            st.info("Data OHLCV tidak tersedia untuk grafik Candlestick.")
            return

        try:
            df_candle = pd.DataFrame({
                'Open': df_ohlcv['Open'][selected_ticker],
                'High': df_ohlcv['High'][selected_ticker],
                'Low': df_ohlcv['Low'][selected_ticker],
                'Close': df_ohlcv['Close'][selected_ticker],
                'Volume': df_ohlcv['Volume'][selected_ticker],
            }).dropna()
        except (KeyError, TypeError):
            st.info(f"Data OHLCV tidak tersedia untuk {selected_ticker}.")
            return

        if df_candle.empty:
            st.info(f"Data kosong untuk {selected_ticker}.")
            return

        # SMA 20
        df_candle['SMA20'] = df_candle['Close'].rolling(window=20).mean()

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.75, 0.25],
        )

        # Candlestick
        fig.add_trace(go.Candlestick(
            x=df_candle.index,
            open=df_candle['Open'],
            high=df_candle['High'],
            low=df_candle['Low'],
            close=df_candle['Close'],
            increasing_line_color='#4ade80',
            decreasing_line_color='#f87171',
            increasing_fillcolor='rgba(74,222,128,0.3)',
            decreasing_fillcolor='rgba(248,113,113,0.3)',
            name='OHLC',
        ), row=1, col=1)

        # SMA 20
        fig.add_trace(go.Scatter(
            x=df_candle.index,
            y=df_candle['SMA20'],
            mode='lines',
            line=dict(color='#a4e6ff', width=1.5, dash='dot'),
            name='SMA 20',
        ), row=1, col=1)

        # Volume bars
        colors_vol = ['rgba(74,222,128,0.4)' if c >= o else 'rgba(248,113,113,0.4)'
                      for c, o in zip(df_candle['Close'], df_candle['Open'])]

        fig.add_trace(go.Bar(
            x=df_candle.index,
            y=df_candle['Volume'],
            marker_color=colors_vol,
            name='Volume',
            showlegend=False,
        ), row=2, col=1)

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Space Grotesk', color='#bbc9cf'),
            xaxis_rangeslider_visible=False,
            xaxis2=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(
                title='Price ($)',
                gridcolor='rgba(255,255,255,0.05)',
                zerolinecolor='rgba(255,255,255,0.1)',
            ),
            yaxis2=dict(
                title='Volume',
                gridcolor='rgba(255,255,255,0.05)',
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                font=dict(size=11, color='#bbc9cf'),
            ),
            margin=dict(l=50, r=20, t=30, b=20),
            height=500,
        )

        st.plotly_chart(fig, width="stretch")


if __name__ == "__main__":
    HalamanSahamTerbaik().render()