import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#  CLASS 1 CandlestickTheme
#  Enkapsulasi semua konstanta warna & styling dark theme STOCKIT

class CandlestickTheme:
    # Warna dasar
    BG       = "#0d1117"
    PANEL    = "#161b22"
    BORDER   = "#30363d"
    TEXT     = "#e6edf3"
    SUBTEXT  = "#8b949e"

    # Warna candle
    BULL     = "#3fb950"               # hijau: harga naik
    BEAR     = "#f85149"               # merah: harga turun

    # Warna Moving Average
    MA20     = "#ffa657"               # orange
    MA50     = "#58a6ff"               # biru
    MA200    = "#bc8cff"               # ungu

    # Warna volume (rgba Plotly-safe)
    VOL_BULL = "rgba(63,185,80,0.4)"
    VOL_BEAR = "rgba(248,81,73,0.4)"

    # Palet warna untuk comparison chart
    PALETTE  = [
        "#58a6ff", "#3fb950", "#ffa657", "#f85149",
        "#bc8cff", "#79c0ff", "#d29922", "#ff7b72",
    ]

    @classmethod
    def axis_style(cls) -> dict:
        return dict(
            gridcolor=cls.BORDER,
            gridwidth=0.5,
            showline=True,
            linecolor=cls.BORDER,
            tickfont=dict(color=cls.SUBTEXT),
            zerolinecolor=cls.BORDER,
        )

    @classmethod
    def legend_style(cls) -> dict:
        return dict(
            bgcolor=cls.PANEL,
            bordercolor=cls.BORDER,
            borderwidth=1,
            font=dict(color=cls.TEXT, size=10),
            orientation="h",
            yanchor="bottom", y=1.01,
            xanchor="left",   x=0,
        )

    @classmethod
    def apply(cls, fig: go.Figure, title: str, ticker: str,
               height: int) -> go.Figure:
        fig.update_layout(
            title=dict(
                text=(f"<b>{title}</b>  "
                      f"<span style='color:{cls.SUBTEXT};"
                      f"font-size:13px;'>{ticker}</span>"),
                font=dict(color=cls.TEXT, size=16),
                x=0.02,
            ),
            height=height,
            paper_bgcolor=cls.BG,
            plot_bgcolor=cls.PANEL,
            font=dict(color=cls.TEXT, family="DejaVu Sans", size=11),
            legend=cls.legend_style(),
            hovermode="x unified",
            xaxis_rangeslider_visible=False,
            margin=dict(l=10, r=10, t=60, b=10),
        )
        fig.update_xaxes(**cls.axis_style())
        fig.update_yaxes(**cls.axis_style(), tickprefix="$")
        return fig


#  CLASS 2 StockDataLoader
#  Load data saham dari Yahoo Finance, fallback ke data sintetis

class StockDataLoader:
    # Harga awal realistis per ticker
    PRICE_MAP = {
        "AAPL": 180, "MSFT": 380, "NVDA": 800, "TSLA": 200,
        "GOOGL": 170, "AMZN": 185, "META": 500, "BRK-B": 400,
        "JPM": 200,  "V": 270,
    }

    # Volatilitas harian per ticker
    SIGMA_MAP = {
        "NVDA": 0.035, "TSLA": 0.038, "META": 0.028,
        "AAPL": 0.018, "MSFT": 0.017, "GOOGL": 0.020,
        "AMZN": 0.022, "BRK-B": 0.012, "JPM": 0.018, "V": 0.015,
    }

    # Mapping period jumlah hari trading
    PERIOD_DAYS = {
        "1mo": 21, "3mo": 63, "6mo": 126,
        "1y": 252, "2y": 504, "5y": 1260,
        "10y": 2520, "21y": 5292, "max": None
    }

    def __init__(self, period: str = "1y", verbose: bool = True):
        self.period  = period
        self.verbose = verbose
        self.n_days  = self.PERIOD_DAYS.get(period, None)

    # Private methods 
    def _log(self, msg: str) -> None:
        """Cetak pesan jika verbose aktif."""
        if self.verbose:
            print(msg)

    def _generate_synthetic(self, ticker: str) -> pd.DataFrame:
        start_price = self.PRICE_MAP.get(ticker.upper(), 100.0)
        sigma       = self.SIGMA_MAP.get(ticker.upper(), 0.020)
        mu          = 0.0003  # ~7.5% drift tahunan

        rng    = np.random.default_rng(abs(hash(ticker)) % (2 ** 31))
        shocks = rng.normal(mu, sigma, size=self.n_days)
        close  = start_price * np.exp(np.cumsum(shocks))

        noise_hl  = rng.uniform(0.005, 0.015, size=self.n_days) * close
        noise_oc  = rng.uniform(0.000, 0.008, size=self.n_days) * close
        direction = rng.choice([-1, 1], size=self.n_days)

        open_  = close - direction * noise_oc
        high   = np.maximum(close, open_) + noise_hl
        low    = np.minimum(close, open_) - noise_hl

        base_vol = self.PRICE_MAP.get(ticker.upper(), 100) * 500_000
        volume   = rng.lognormal(np.log(base_vol), 0.4,
                                  size=self.n_days).astype(int)

        dates = pd.bdate_range(
            end=pd.Timestamp.today().normalize(), periods=self.n_days
        )
        df = pd.DataFrame({
            "Open": open_, "High": high,
            "Low": low, "Close": close, "Volume": volume,
        }, index=dates)
        df.index.name = "Date"
        return df

    @staticmethod
    def _normalize(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.columns.name = None
        return df

    @staticmethod
    def _clean_tz(df: pd.DataFrame) -> pd.DataFrame:
        if hasattr(df.index, "tz") and df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        return df

    def _load_from_parquet(self, tickers: list) -> dict:
        import os
        import pandas as pd

        self._log(f"Memuat {len(tickers)} ticker dari file Parquet lokal...")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        raw_dir = os.path.join(base_dir, 'Data', 'Raw')
        
        dfs = {}
        for t in tickers:
            file_path = os.path.join(raw_dir, f"{t.upper()}.parquet")
            if os.path.exists(file_path):
                df = pd.read_parquet(file_path)
                df = self._clean_tz(df)
                
                # Slicing berdasarkan periode (jika bukan max)
                if self.period != 'max' and self.n_days is not None:
                    df = df.tail(self.n_days)
                    
                dfs[t] = df
            else:
                self._log(f"    [TIDAK DITEMUKAN] File {t} tidak ada di folder Raw.")
                raise FileNotFoundError(f"Data {t} belum di-pull oleh pipeline.")
                
        ok = [t for t in tickers if t in dfs and not dfs[t].empty]
        self._log(f"  Load OK: {ok}")
        return dfs

    # Public method 
    def load(self, tickers) -> dict:
        if isinstance(tickers, str):
            tickers = [tickers]

        try:
            return self._load_from_parquet(tickers)

        except Exception as e:
            self._log(f"  Download gagal: {e}")
            self._log("  Menggunakan data SINTETIS untuk demo...")

            dfs = {}
            for t in tickers:
                dfs[t] = self._generate_synthetic(t)
                self._log(f"    [SYNTHETIC] {t}: {self.n_days} hari")
            return dfs


#  CLASS 3 CandlestickChart
#  Membangun single interactive candlestick chart

class CandlestickChart:
    def __init__(
        self,
        df: pd.DataFrame,
        ticker: str,
        title: str = None,
        *,
        show_volume: bool = True,
        show_ma20: bool = True,
        show_ma50: bool = True,
        show_ma200: bool = False,
        height: int = None,
        date_from: str = None,
        date_to: str = None,
    ):
        self.ticker      = ticker
        self.title       = title or ticker
        self.show_volume = show_volume
        self.show_ma20   = show_ma20
        self.show_ma50   = show_ma50
        self.show_ma200  = show_ma200
        self.height      = height
        self.date_from   = date_from
        self.date_to     = date_to
        self.theme       = CandlestickTheme()

        # Proses DataFrame
        self.df = self._prepare(df)

    # Private helpers 

    def _prepare(self, df: pd.DataFrame) -> pd.DataFrame:
        df = StockDataLoader._normalize(df)

        # Validasi kolom wajib
        required = {"Open", "High", "Low", "Close"}
        missing  = required - set(df.columns)
        if missing:
            raise ValueError(
                f"DataFrame kurang kolom: {missing}\n"
                f"Kolom tersedia: {list(df.columns)}"
            )

        df = StockDataLoader._clean_tz(df)

        # Filter tanggal
        if self.date_from:
            df = df[df.index >= pd.Timestamp(self.date_from)]
        if self.date_to:
            df = df[df.index <= pd.Timestamp(self.date_to)]

        if df.empty:
            raise ValueError("DataFrame kosong setelah filter tanggal.")
        return df

    def _make_subplots(self, has_vol: bool) -> go.Figure:
        if has_vol:
            return make_subplots(
                rows=2, cols=1, shared_xaxes=True,
                vertical_spacing=0.03, row_heights=[0.75, 0.25],
            )
        return make_subplots(rows=1, cols=1)

    def _add_candlestick(self, fig: go.Figure) -> go.Figure:
        fig.add_trace(go.Candlestick(
            x=self.df.index,
            open=self.df["Open"], high=self.df["High"],
            low=self.df["Low"],   close=self.df["Close"],
            name=self.ticker,
            increasing=dict(
                line=dict(color=CandlestickTheme.BULL, width=1),
                fillcolor=CandlestickTheme.BULL,
            ),
            decreasing=dict(
                line=dict(color=CandlestickTheme.BEAR, width=1),
                fillcolor=CandlestickTheme.BEAR,
            ),
        ), row=1, col=1)
        return fig

    def _add_moving_averages(self, fig: go.Figure) -> go.Figure:
        ma_config = [
            (self.show_ma20,  20,  "MA20",  CandlestickTheme.MA20),
            (self.show_ma50,  50,  "MA50",  CandlestickTheme.MA50),
            (self.show_ma200, 200, "MA200", CandlestickTheme.MA200),
        ]
        for enabled, window, name, color in ma_config:
            if enabled and len(self.df) >= window:
                fig.add_trace(go.Scatter(
                    x=self.df.index,
                    y=self.df["Close"].rolling(window).mean(),
                    name=name,
                    line=dict(color=color, width=1.2),
                    opacity=0.85,
                    hovertemplate=f"{name}: $%{{y:,.2f}}<extra></extra>",
                ), row=1, col=1)
        return fig

    def _add_volume(self, fig: go.Figure) -> go.Figure:
        colors = [
            CandlestickTheme.VOL_BULL if c >= o else CandlestickTheme.VOL_BEAR
            for c, o in zip(self.df["Close"], self.df["Open"])
        ]
        fig.add_trace(go.Bar(
            x=self.df.index, y=self.df["Volume"],
            name="Volume",
            marker_color=colors,
            marker_line_width=0,
            hovertemplate="Vol: %{y:,.0f}<extra></extra>",
        ), row=2, col=1)
        fig.update_yaxes(
            title_text="Volume",
            title_font=dict(color=CandlestickTheme.SUBTEXT, size=10),
            tickprefix="", row=2, col=1,
        )
        return fig

    def _add_annotations(self, fig: go.Figure) -> go.Figure:
        last_close  = float(self.df["Close"].iloc[-1])
        last_open   = float(self.df["Open"].iloc[-1])
        first_close = float(self.df["Close"].iloc[0])
        last_date   = self.df.index[-1]

        # Anotasi harga
        clr = CandlestickTheme.BULL if last_close >= last_open else CandlestickTheme.BEAR
        fig.add_annotation(
            x=last_date, y=last_close,
            text=f"  ${last_close:,.2f}",
            showarrow=False,
            font=dict(color=clr, size=12, family="DejaVu Sans"),
            xanchor="left", yanchor="middle",
            row=1, col=1,
        )

        # Anotasi return %
        total_ret = (last_close / first_close - 1) * 100
        ret_color = CandlestickTheme.BULL if total_ret >= 0 else CandlestickTheme.BEAR
        sign      = "+" if total_ret >= 0 else ""
        fig.add_annotation(
            x=0.99, y=0.99, xref="paper", yref="paper",
            text=f"Return: <b style='color:{ret_color}'>{sign}{total_ret:.2f}%</b>",
            showarrow=False,
            font=dict(color=CandlestickTheme.TEXT, size=11),
            align="right", xanchor="right", yanchor="top",
            bgcolor=CandlestickTheme.PANEL,
            bordercolor=CandlestickTheme.BORDER,
            borderwidth=1, borderpad=6,
        )
        return fig

    # Public methods 

    def build(self) -> go.Figure:
        has_vol = self.show_volume and "Volume" in self.df.columns
        height  = self.height or (720 if has_vol else 600)

        fig = self._make_subplots(has_vol)
        fig = self._add_candlestick(fig)
        fig = self._add_moving_averages(fig)

        if has_vol:
            fig = self._add_volume(fig)

        fig = self._add_annotations(fig)
        fig = CandlestickTheme.apply(fig, self.title, self.ticker, height)

        # Hapus prefix $ dari sumbu volume
        if has_vol:
            fig.update_yaxes(tickprefix="", row=2, col=1)

        return fig

    def show(self) -> None:
        self.build().show()


#  CLASS 4 ComparisonChart
#  Perbandingan beberapa saham (normalized close price)

class ComparisonChart:
    def __init__(
        self,
        data_dict: dict,
        title: str = "Perbandingan Saham",
        *,
        height: int = 500,
        date_from: str = None,
        date_to: str = None,
    ):
        self.data_dict = data_dict
        self.title     = title
        self.height    = height
        self.date_from = date_from
        self.date_to   = date_to

    def _filter(self, df: pd.DataFrame) -> pd.DataFrame:
        df = StockDataLoader._normalize(df.copy())
        df = StockDataLoader._clean_tz(df)
        if self.date_from:
            df = df[df.index >= pd.Timestamp(self.date_from)]
        if self.date_to:
            df = df[df.index <= pd.Timestamp(self.date_to)]
        return df

    def build(self) -> go.Figure:
        fig = go.Figure()

        for i, (ticker, df) in enumerate(self.data_dict.items()):
            df = self._filter(df)
            if df.empty or "Close" not in df.columns:
                continue

            normalized = df["Close"] / df["Close"].iloc[0] * 100
            color      = CandlestickTheme.PALETTE[i % len(CandlestickTheme.PALETTE)]

            fig.add_trace(go.Scatter(
                x=df.index, y=normalized,
                name=ticker,
                line=dict(color=color, width=1.8),
                hovertemplate=f"{ticker}: %{{y:.2f}}<extra></extra>",
            ))

        fig.add_hline(
            y=100,
            line_dash="dash",
            line_color=CandlestickTheme.BORDER,
            line_width=1,
        )

        t = CandlestickTheme
        fig.update_layout(
            title=dict(
                text=(f"<b>{self.title}</b>  "
                      f"<span style='color:{t.SUBTEXT};font-size:12px;'>"
                      f"(Normalized, Base = 100)</span>"),
                font=dict(color=t.TEXT, size=15), x=0.02,
            ),
            height=self.height,
            paper_bgcolor=t.BG, plot_bgcolor=t.PANEL,
            font=dict(color=t.TEXT, family="DejaVu Sans", size=11),
            legend=t.legend_style(),
            hovermode="x unified",
            margin=dict(l=10, r=10, t=60, b=10),
            xaxis=dict(
                gridcolor=t.BORDER, showline=True,
                linecolor=t.BORDER, tickfont=dict(color=t.SUBTEXT),
            ),
            yaxis=dict(
                gridcolor=t.BORDER, showline=True,
                linecolor=t.BORDER, tickfont=dict(color=t.SUBTEXT),
                title="Return Index (Base=100)",
                title_font=dict(color=t.SUBTEXT, size=10),
            ),
        )
        return fig

    def show(self) -> None:
        self.build().show()


#  FUNGSI WRAPPER (backward-compatible)
#  Agar notebook tidak perlu diubah: fungsi lama tetap bekerja

def load_stock_data(tickers, period: str = "1y",
                    verbose: bool = True) -> dict:
    return StockDataLoader(period=period, verbose=verbose).load(tickers)


def plot_candlestick(
    df: pd.DataFrame,
    ticker: str,
    title: str = None,
    *,
    show_volume: bool = True,
    show_ma20: bool = True,
    show_ma50: bool = True,
    show_ma200: bool = False,
    height: int = None,
    date_from: str = None,
    date_to: str = None,
) -> go.Figure:
    return CandlestickChart(
        df, ticker, title,
        show_volume=show_volume,
        show_ma20=show_ma20, show_ma50=show_ma50, show_ma200=show_ma200,
        height=height, date_from=date_from, date_to=date_to,
    ).build()


def plot_candlestick_comparison(
    data_dict: dict,
    title: str = "Perbandingan Saham",
    *,
    height: int = 500,
    date_from: str = None,
    date_to: str = None,
) -> go.Figure:
    return ComparisonChart(
        data_dict, title,
        height=height, date_from=date_from, date_to=date_to,
    ).build()
