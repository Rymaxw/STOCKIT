import warnings
warnings.filterwarnings("ignore")

import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from Utils.indikator import PenghitungIndikator


class TemaCandlestick:
    LATAR       = "#0d1117"
    PANEL       = "#161b22"
    BATAS       = "#30363d"
    TEKS        = "#e6edf3"
    TEKS_TIPIS  = "#8b949e"
    NAIK        = "#3fb950"   
    TURUN       = "#f85149"   
    MA5         = "#79c0ff"   
    MA20        = "#ffa657"   
    MA50        = "#58a6ff"   
    MA200       = "#bc8cff"  
    VOL_NAIK    = "rgba(63,185,80,0.4)"
    VOL_TURUN   = "rgba(248,81,73,0.4)"
    BOLLINGER   = "rgba(139, 148, 158, 0.12)"
    RSI         = "#bc8cff"
    MACD        = "#58a6ff"
    MACD_SINYAL = "#ffa657"
    ATR         = "#79c0ff"
    VOLATILITAS = "#ff7b72"

    PALET       = [
        "#58a6ff", "#3fb950", "#ffa657", "#f85149",
        "#bc8cff", "#79c0ff", "#d29922", "#ff7b72",
    ]

    @classmethod
    def gaya_sumbu(cls) -> dict:
        return dict(
            gridcolor=cls.BATAS,
            gridwidth=0.5,
            showline=True,
            linecolor=cls.BATAS,
            tickfont=dict(color=cls.TEKS_TIPIS),
            zerolinecolor=cls.BATAS,
        )

    @classmethod
    def gaya_legenda(cls) -> dict:
        return dict(
            bgcolor=cls.PANEL,
            bordercolor=cls.BATAS,
            borderwidth=1,
            font=dict(color=cls.TEKS, size=10),
            orientation="h",
            yanchor="bottom", y=1.01,
            xanchor="left",   x=0,
        )

    @classmethod
    def terapkan(cls, fig: go.Figure, judul: str, kode_saham: str, tinggi: int) -> go.Figure:
        fig.update_layout(
            title=dict(
                text=(f"<b>{judul}</b>  "
                      f"<span style='color:{cls.TEKS_TIPIS};"
                      f"font-size:13px;'>{kode_saham}</span>"),
                font=dict(color=cls.TEKS, size=16),
                x=0.02,
            ),
            height=tinggi,
            paper_bgcolor=cls.LATAR,
            plot_bgcolor=cls.PANEL,
            font=dict(color=cls.TEKS, family="DejaVu Sans", size=11),
            legend=cls.gaya_legenda(),
            hovermode="x unified",
            xaxis_rangeslider_visible=False,
            margin=dict(l=10, r=10, t=60, b=10),
        )
        fig.update_xaxes(**cls.gaya_sumbu())
        fig.update_yaxes(**cls.gaya_sumbu(), tickprefix="$")
        return fig


class PemuatDataSaham:


    PETA_HARGA = {
        "AAPL": 180, "MSFT": 380, "NVDA": 800, "TSLA": 200,
        "GOOGL": 170, "AMZN": 185, "META": 500, "BRK-B": 400,
        "JPM": 200,   "V": 270,
    }


    PETA_SIGMA = {
        "NVDA": 0.035, "TSLA": 0.038, "META": 0.028,
        "AAPL": 0.018, "MSFT": 0.017, "GOOGL": 0.020,
        "AMZN": 0.022, "BRK-B": 0.012, "JPM": 0.018, "V": 0.015,
    }


    PETA_HARI = {
        "1mo": 21, "3mo": 63, "6mo": 126,
        "1y": 252, "2y": 504, "5y": 1260,
        "10y": 2520, "21y": 5292, "max": None,
    }

    def __init__(self, periode: str = "1y", verbose: bool = True):
        self.periode = periode
        self.verbose = verbose
        self.jumlah_hari = self.PETA_HARI.get(periode, None)

    def _log(self, pesan: str) -> None:
        if self.verbose:
            print(pesan)

    def _buat_data_sintetis(self, kode_saham: str) -> pd.DataFrame:
        harga_awal = self.PETA_HARGA.get(kode_saham.upper(), 100.0)
        sigma      = self.PETA_SIGMA.get(kode_saham.upper(), 0.020)
        mu         = 0.0003

        rng       = np.random.default_rng(abs(hash(kode_saham)) % (2 ** 31))
        guncangan = rng.normal(mu, sigma, size=self.jumlah_hari)
        harga_close = harga_awal * np.exp(np.cumsum(guncangan))

        noise_hl  = rng.uniform(0.005, 0.015, size=self.jumlah_hari) * harga_close
        noise_oc  = rng.uniform(0.000, 0.008, size=self.jumlah_hari) * harga_close
        arah      = rng.choice([-1, 1], size=self.jumlah_hari)

        harga_open = harga_close - arah * noise_oc
        harga_high = np.maximum(harga_close, harga_open) + noise_hl
        harga_low  = np.minimum(harga_close, harga_open) - noise_hl

        vol_dasar = self.PETA_HARGA.get(kode_saham.upper(), 100) * 500_000
        volume    = rng.lognormal(np.log(vol_dasar), 0.4, size=self.jumlah_hari).astype(int)

        tanggal = pd.bdate_range(
            end=pd.Timestamp.today().normalize(), periods=self.jumlah_hari
        )
        df = pd.DataFrame({
            "Open": harga_open, "High": harga_high,
            "Low": harga_low, "Close": harga_close, "Volume": volume,
        }, index=tanggal)
        df.index.name = "Date"
        return df

    @staticmethod
    def _normalisasi_kolom(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.columns.name = None
        return df

    @staticmethod
    def _hapus_timezone(df: pd.DataFrame) -> pd.DataFrame:
        if hasattr(df.index, "tz") and df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        return df

    def _muat_dari_parquet(self, daftar_ticker: list) -> dict:
        self._log(f"Memuat {len(daftar_ticker)} ticker dari file Parquet lokal...")

        folder_utama = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder_raw   = os.path.join(folder_utama, 'Data', 'Raw')

        dfs = {}
        for ticker in daftar_ticker:
            lokasi_berkas = os.path.join(folder_raw, f"{ticker.upper()}.parquet")
            if os.path.exists(lokasi_berkas):
                df = pd.read_parquet(lokasi_berkas)
                df = self._hapus_timezone(df)
                if self.periode != 'max' and self.jumlah_hari is not None:
                    df = df.tail(self.jumlah_hari)
                dfs[ticker] = df
            else:
                self._log(f"  [TIDAK DITEMUKAN] File {ticker} tidak ada di folder Raw.")
                raise FileNotFoundError(f"Data {ticker} belum di-pull oleh pipeline.")

        ok = [t for t in daftar_ticker if t in dfs and not dfs[t].empty]
        self._log(f"  Load OK: {ok}")
        return dfs

    def muat(self, daftar_ticker) -> dict:
        if isinstance(daftar_ticker, str):
            daftar_ticker = [daftar_ticker]

        try:
            return self._muat_dari_parquet(daftar_ticker)
        except Exception as galat:
            self._log(f"  Load gagal: {galat}")
            self._log("  Menggunakan data SINTETIS untuk demo...")

            dfs = {}
            for ticker in daftar_ticker:
                dfs[ticker] = self._buat_data_sintetis(ticker)
                self._log(f"  [SINTETIS] {ticker}: {self.jumlah_hari} hari")
            return dfs


class GrafikCandlestick:

    def __init__(
        self,
        df: pd.DataFrame,
        kode_saham: str,
        judul: str = None,
        *,
        tampilkan_volume: bool = True,
        tampilkan_ma5: bool = False,
        tampilkan_ma20: bool = True,
        tampilkan_ma50: bool = True,
        tampilkan_ma200: bool = False,
        tampilkan_bollinger: bool = False,
        tampilkan_rsi: bool = False,
        tampilkan_macd: bool = False,
        tampilkan_atr: bool = False,
        tampilkan_volatilitas: bool = False,
        tinggi: int = None,
        tanggal_dari: str = None,
        tanggal_sampai: str = None,
    ):
        self.kode_saham            = kode_saham
        self.judul                 = judul or kode_saham
        self.tampilkan_volume      = tampilkan_volume
        self.tampilkan_ma5         = tampilkan_ma5
        self.tampilkan_ma20        = tampilkan_ma20
        self.tampilkan_ma50        = tampilkan_ma50
        self.tampilkan_ma200       = tampilkan_ma200
        self.tampilkan_bollinger   = tampilkan_bollinger
        self.tampilkan_rsi         = tampilkan_rsi
        self.tampilkan_macd        = tampilkan_macd
        self.tampilkan_atr         = tampilkan_atr
        self.tampilkan_volatilitas = tampilkan_volatilitas
        self.tinggi                = tinggi
        self.tanggal_dari          = tanggal_dari
        self.tanggal_sampai        = tanggal_sampai
        self.tema                  = TemaCandlestick()

        self.df = self._siapkan_data(df)

    def _siapkan_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = PemuatDataSaham._normalisasi_kolom(df)

        kolom_wajib = {"Open", "High", "Low", "Close"}
        kolom_kurang = kolom_wajib - set(df.columns)
        if kolom_kurang:
            raise ValueError(
                f"DataFrame kurang kolom: {kolom_kurang}\n"
                f"Kolom tersedia: {list(df.columns)}"
            )

        df = PemuatDataSaham._hapus_timezone(df)

        if self.tanggal_dari:
            df = df[df.index >= pd.Timestamp(self.tanggal_dari)]
        if self.tanggal_sampai:
            df = df[df.index <= pd.Timestamp(self.tanggal_sampai)]

        if df.empty:
            raise ValueError("DataFrame kosong setelah filter tanggal.")

        # Fallback dinamis jika indikator belum dihitung di dataset
        df = df.copy()
        if 'MA5' not in df.columns:
            df['MA5'] = PenghitungIndikator.hitung_rerata_bergerak(df, jendela=5)
        if 'MA20' not in df.columns:
            df['MA20'] = PenghitungIndikator.hitung_rerata_bergerak(df, jendela=20)
        if 'MA50' not in df.columns:
            df['MA50'] = PenghitungIndikator.hitung_rerata_bergerak(df, jendela=50)
        if 'MA200' not in df.columns:
            df['MA200'] = PenghitungIndikator.hitung_rerata_bergerak(df, jendela=200)
        if 'RSI_14' not in df.columns:
            df['RSI_14'] = PenghitungIndikator.hitung_rsi(df, jendela=14)
        if 'MACD_Garis' not in df.columns:
            df_macd = PenghitungIndikator.hitung_macd(df)
            df['MACD_Garis'] = df_macd['MACD_Garis']
            df['MACD_Sinyal'] = df_macd['MACD_Sinyal']
            df['MACD_Histogram'] = df_macd['MACD_Histogram']
        if 'Bollinger_Atas' not in df.columns:
            df_bb = PenghitungIndikator.hitung_pita_bollinger(df)
            df['Bollinger_Atas'] = df_bb['Bollinger_Atas']
            df['Bollinger_Tengah'] = df_bb['Bollinger_Tengah']
            df['Bollinger_Bawah'] = df_bb['Bollinger_Bawah']
        if 'ATR_14' not in df.columns:
            df['ATR_14'] = PenghitungIndikator.hitung_atr(df, jendela=14)
        if 'Volatilitas_30H' not in df.columns:
            df['Volatilitas_30H'] = PenghitungIndikator.hitung_volatilitas_bergulir(df, jendela=30)

        return df

    def _buat_layout_dan_subplots(self) -> tuple[go.Figure, dict]:
        baris_aktif = [("utama", 0.50)]
        
        ada_volume = self.tampilkan_volume and "Volume" in self.df.columns
        if ada_volume:
            baris_aktif.append(("volume", 0.15))
        if self.tampilkan_rsi:
            baris_aktif.append(("rsi", 0.15))
        if self.tampilkan_macd:
            baris_aktif.append(("macd", 0.18))
        if self.tampilkan_atr:
            baris_aktif.append(("atr", 0.12))
        if self.tampilkan_volatilitas:
            baris_aktif.append(("volatilitas", 0.12))
            
        # Hitung tinggi baris
        if len(baris_aktif) == 1:
            row_heights = [1.0]
        else:
            total_tambahan = sum(b for l, b in baris_aktif[1:])
            tinggi_utama = max(0.40, 1.0 - total_tambahan)
            row_heights = [tinggi_utama] + [b for l, b in baris_aktif[1:]]
            
            # Normalisasi
            total = sum(row_heights)
            row_heights = [h / total for h in row_heights]
            
        fig = make_subplots(
            rows=len(baris_aktif),
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=row_heights
        )
        
        peta_baris = {label: index for index, (label, _) in enumerate(baris_aktif, 1)}
        return fig, peta_baris

    def _tambah_candlestick(self, fig: go.Figure, row: int) -> go.Figure:
        fig.add_trace(go.Candlestick(
            x=self.df.index,
            open=self.df["Open"], high=self.df["High"],
            low=self.df["Low"],   close=self.df["Close"],
            name=self.kode_saham,
            increasing=dict(
                line=dict(color=TemaCandlestick.NAIK, width=1),
                fillcolor=TemaCandlestick.NAIK,
            ),
            decreasing=dict(
                line=dict(color=TemaCandlestick.TURUN, width=1),
                fillcolor=TemaCandlestick.TURUN,
            ),
        ), row=row, col=1)
        return fig

    def _tambah_moving_average(self, fig: go.Figure, row: int) -> go.Figure:
        konfigurasi_ma = [
            (self.tampilkan_ma5,   5,   "MA5",   TemaCandlestick.MA5),
            (self.tampilkan_ma20,  20,  "MA20",  TemaCandlestick.MA20),
            (self.tampilkan_ma50,  50,  "MA50",  TemaCandlestick.MA50),
            (self.tampilkan_ma200, 200, "MA200", TemaCandlestick.MA200),
        ]
        for aktif, jendela, nama, warna in konfigurasi_ma:
            if aktif and len(self.df) >= jendela:
                fig.add_trace(go.Scatter(
                    x=self.df.index,
                    y=self.df[nama],
                    name=nama,
                    line=dict(color=warna, width=1.2),
                    opacity=0.85,
                    hovertemplate=f"{nama}: $%{{y:,.2f}}<extra></extra>",
                ), row=row, col=1)
        return fig

    def _tambah_bollinger_bands(self, fig: go.Figure, row: int) -> go.Figure:
        # BB Atas
        fig.add_trace(go.Scatter(
            x=self.df.index, y=self.df["Bollinger_Atas"],
            name="BB Atas",
            line=dict(color=TemaCandlestick.BOLLINGER, width=0.8),
            legendgroup="BB",
            showlegend=False,
            hovertemplate="BB Atas: $%{y:,.2f}<extra></extra>",
        ), row=row, col=1)
        
        # BB Bawah (diarsir ke BB Atas)
        fig.add_trace(go.Scatter(
            x=self.df.index, y=self.df["Bollinger_Bawah"],
            name="Pita Bollinger",
            line=dict(color=TemaCandlestick.BOLLINGER, width=0.8),
            fill='tonexty',
            fillcolor="rgba(139, 148, 158, 0.04)",
            legendgroup="BB",
            hovertemplate="BB Bawah: $%{y:,.2f}<extra></extra>",
        ), row=row, col=1)
        
        # BB Tengah
        fig.add_trace(go.Scatter(
            x=self.df.index, y=self.df["Bollinger_Tengah"],
            name="BB Tengah",
            line=dict(color=TemaCandlestick.BOLLINGER, width=1.0, dash='dash'),
            legendgroup="BB",
            showlegend=False,
            hovertemplate="BB Tengah: $%{y:,.2f}<extra></extra>",
        ), row=row, col=1)
        
        return fig

    def _tambah_volume(self, fig: go.Figure, row: int) -> go.Figure:
        daftar_warna = [
            TemaCandlestick.VOL_NAIK if c >= o else TemaCandlestick.VOL_TURUN
            for c, o in zip(self.df["Close"], self.df["Open"])
        ]
        fig.add_trace(go.Bar(
            x=self.df.index, y=self.df["Volume"],
            name="Volume",
            marker_color=daftar_warna,
            marker_line_width=0,
            hovertemplate="Vol: %{y:,.0f}<extra></extra>",
        ), row=row, col=1)
        fig.update_yaxes(
            title_text="Volume",
            title_font=dict(color=TemaCandlestick.TEKS_TIPIS, size=10),
            tickprefix="", row=row, col=1,
        )
        return fig

    def _tambah_rsi(self, fig: go.Figure, row: int) -> go.Figure:
        fig.add_trace(go.Scatter(
            x=self.df.index, y=self.df["RSI_14"],
            name="RSI (14)",
            line=dict(color=TemaCandlestick.RSI, width=1.5),
            hovertemplate="RSI: %{y:.2f}<extra></extra>",
        ), row=row, col=1)
        
        # Garis oversold (30) dan overbought (70)
        fig.add_hline(y=70, line_dash="dash", line_color="#f85149", line_width=1, row=row, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#3fb950", line_width=1, row=row, col=1)
        fig.add_hrect(y0=30, y1=70, fillcolor="rgba(188, 140, 255, 0.03)", line_width=0, row=row, col=1)
        
        fig.update_yaxes(
            title_text="RSI",
            title_font=dict(color=TemaCandlestick.TEKS_TIPIS, size=10),
            tickvals=[30, 50, 70],
            range=[10, 90],
            row=row, col=1
        )
        return fig

    def _tambah_macd(self, fig: go.Figure, row: int) -> go.Figure:
        # MACD Line
        fig.add_trace(go.Scatter(
            x=self.df.index, y=self.df["MACD_Garis"],
            name="MACD",
            line=dict(color=TemaCandlestick.MACD, width=1.5),
            hovertemplate="MACD: %{y:.3f}<extra></extra>",
        ), row=row, col=1)
        
        # Signal Line
        fig.add_trace(go.Scatter(
            x=self.df.index, y=self.df["MACD_Sinyal"],
            name="Sinyal",
            line=dict(color=TemaCandlestick.MACD_SINYAL, width=1.2),
            hovertemplate="Sinyal: %{y:.3f}<extra></extra>",
        ), row=row, col=1)
        
        # Histogram
        warna_histo = [
            TemaCandlestick.NAIK if val >= 0 else TemaCandlestick.TURUN 
            for val in self.df["MACD_Histogram"]
        ]
        fig.add_trace(go.Bar(
            x=self.df.index, y=self.df["MACD_Histogram"],
            name="Histogram",
            marker_color=warna_histo,
            marker_line_width=0,
            hovertemplate="Histo: %{y:.3f}<extra></extra>",
        ), row=row, col=1)
        
        fig.update_yaxes(
            title_text="MACD",
            title_font=dict(color=TemaCandlestick.TEKS_TIPIS, size=10),
            row=row, col=1
        )
        return fig

    def _tambah_atr(self, fig: go.Figure, row: int) -> go.Figure:
        fig.add_trace(go.Scatter(
            x=self.df.index, y=self.df["ATR_14"],
            name="ATR (14)",
            line=dict(color=TemaCandlestick.ATR, width=1.5),
            hovertemplate="ATR: %{y:,.3f}<extra></extra>",
        ), row=row, col=1)
        
        fig.update_yaxes(
            title_text="ATR",
            title_font=dict(color=TemaCandlestick.TEKS_TIPIS, size=10),
            row=row, col=1
        )
        return fig

    def _tambah_volatilitas(self, fig: go.Figure, row: int) -> go.Figure:
        fig.add_trace(go.Scatter(
            x=self.df.index, y=self.df["Volatilitas_30H"] * 100,
            name="Volatilitas 30H",
            line=dict(color=TemaCandlestick.VOLATILITAS, width=1.5),
            hovertemplate="Vol 30H: %{y:.2f}%<extra></extra>",
        ), row=row, col=1)
        
        fig.update_yaxes(
            title_text="Vol (%)",
            title_font=dict(color=TemaCandlestick.TEKS_TIPIS, size=10),
            row=row, col=1
        )
        return fig

    def _tambah_anotasi(self, fig: go.Figure) -> go.Figure:
        harga_terakhir = float(self.df["Close"].iloc[-1])
        harga_buka     = float(self.df["Open"].iloc[-1])
        harga_pertama  = float(self.df["Close"].iloc[0])
        tanggal_akhir  = self.df.index[-1]

        warna = TemaCandlestick.NAIK if harga_terakhir >= harga_buka else TemaCandlestick.TURUN
        fig.add_annotation(
            x=tanggal_akhir, y=harga_terakhir,
            text=f"  ${harga_terakhir:,.2f}",
            showarrow=False,
            font=dict(color=warna, size=12, family="DejaVu Sans"),
            xanchor="left", yanchor="middle",
            row=1, col=1,
        )

        total_return = (harga_terakhir / harga_pertama - 1) * 100
        warna_return = TemaCandlestick.NAIK if total_return >= 0 else TemaCandlestick.TURUN
        tanda        = "+" if total_return >= 0 else ""
        fig.add_annotation(
            x=0.99, y=0.99, xref="paper", yref="paper",
            text=f"Return: <b style='color:{warna_return}'>{tanda}{total_return:.2f}%</b>",
            showarrow=False,
            font=dict(color=TemaCandlestick.TEKS, size=11),
            align="right", xanchor="right", yanchor="top",
            bgcolor=TemaCandlestick.PANEL,
            bordercolor=TemaCandlestick.BATAS,
            borderwidth=1, borderpad=6,
        )
        return fig

    def bangun(self) -> go.Figure:
        fig, peta_baris = self._buat_layout_dan_subplots()
        
        # Panel utama
        r_utama = peta_baris["utama"]
        fig = self._tambah_candlestick(fig, r_utama)
        fig = self._tambah_moving_average(fig, r_utama)
        
        if self.tampilkan_bollinger:
            fig = self._tambah_bollinger_bands(fig, r_utama)
            
        # Panel tambahan
        if "volume" in peta_baris:
            fig = self._tambah_volume(fig, peta_baris["volume"])
        if "rsi" in peta_baris:
            fig = self._tambah_rsi(fig, peta_baris["rsi"])
        if "macd" in peta_baris:
            fig = self._tambah_macd(fig, peta_baris["macd"])
        if "atr" in peta_baris:
            fig = self._tambah_atr(fig, peta_baris["atr"])
        if "volatilitas" in peta_baris:
            fig = self._tambah_volatilitas(fig, peta_baris["volatilitas"])

        fig = self._tambah_anotasi(fig)
        
        # Tentukan tinggi chart
        tinggi_dasar = 600
        tinggi_akhir = self.tinggi or (tinggi_dasar + 120 * (len(peta_baris) - 1))
        
        fig = TemaCandlestick.terapkan(fig, self.judul, self.kode_saham, tinggi_akhir)
        return fig

    def tampilkan(self) -> None:
        self.bangun().show()


class GrafikKomparasi:

    def __init__(
        self,
        dict_data: dict,
        judul: str = "Perbandingan Saham",
        *,
        tinggi: int = 500,
        tanggal_dari: str = None,
        tanggal_sampai: str = None,
    ):
        self.dict_data      = dict_data
        self.judul          = judul
        self.tinggi         = tinggi
        self.tanggal_dari   = tanggal_dari
        self.tanggal_sampai = tanggal_sampai

    def _filter_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = PemuatDataSaham._normalisasi_kolom(df.copy())
        df = PemuatDataSaham._hapus_timezone(df)
        if self.tanggal_dari:
            df = df[df.index >= pd.Timestamp(self.tanggal_dari)]
        if self.tanggal_sampai:
            df = df[df.index <= pd.Timestamp(self.tanggal_sampai)]
        return df

    def bangun(self) -> go.Figure:
        fig = go.Figure()

        for urutan, (kode_saham, df) in enumerate(self.dict_data.items()):
            df = self._filter_data(df)
            if df.empty or "Close" not in df.columns:
                continue

            harga_dinormalisasi = df["Close"] / df["Close"].iloc[0] * 100
            warna = TemaCandlestick.PALET[urutan % len(TemaCandlestick.PALET)]

            fig.add_trace(go.Scatter(
                x=df.index, y=harga_dinormalisasi,
                name=kode_saham,
                line=dict(color=warna, width=1.8),
                hovertemplate=f"{kode_saham}: %{{y:.2f}}<extra></extra>",
            ))

        fig.add_hline(
            y=100,
            line_dash="dash",
            line_color=TemaCandlestick.BATAS,
            line_width=1,
        )

        t = TemaCandlestick
        fig.update_layout(
            title=dict(
                text=(f"<b>{self.judul}</b>  "
                      f"<span style='color:{t.TEKS_TIPIS};font-size:12px;'>"
                      f"(Normalized, Base = 100)</span>"),
                font=dict(color=t.TEKS, size=15), x=0.02,
            ),
            height=self.tinggi,
            paper_bgcolor=t.LATAR, plot_bgcolor=t.PANEL,
            font=dict(color=t.TEKS, family="DejaVu Sans", size=11),
            legend=t.gaya_legenda(),
            hovermode="x unified",
            margin=dict(l=10, r=10, t=60, b=10),
            xaxis=dict(
                gridcolor=t.BATAS, showline=True,
                linecolor=t.BATAS, tickfont=dict(color=t.TEKS_TIPIS),
            ),
            yaxis=dict(
                gridcolor=t.BATAS, showline=True,
                linecolor=t.BATAS, tickfont=dict(color=t.TEKS_TIPIS),
                title="Return Index (Base=100)",
                title_font=dict(color=t.TEKS_TIPIS, size=10),
            ),
        )
        return fig

    def tampilkan(self) -> None:
        self.bangun().show()


def muat_data_saham(daftar_ticker, periode: str = "1y", verbose: bool = True) -> dict:
    return PemuatDataSaham(periode=periode, verbose=verbose).muat(daftar_ticker)


def buat_grafik_candlestick(
    df: pd.DataFrame,
    kode_saham: str,
    judul: str = None,
    *,
    tampilkan_volume: bool = True,
    tampilkan_ma5: bool = False,
    tampilkan_ma20: bool = True,
    tampilkan_ma50: bool = True,
    tampilkan_ma200: bool = False,
    tampilkan_bollinger: bool = False,
    tampilkan_rsi: bool = False,
    tampilkan_macd: bool = False,
    tampilkan_atr: bool = False,
    tampilkan_volatilitas: bool = False,
    tinggi: int = None,
    tanggal_dari: str = None,
    tanggal_sampai: str = None,
) -> go.Figure:
    return GrafikCandlestick(
        df, kode_saham, judul,
        tampilkan_volume=tampilkan_volume,
        tampilkan_ma5=tampilkan_ma5,
        tampilkan_ma20=tampilkan_ma20,
        tampilkan_ma50=tampilkan_ma50,
        tampilkan_ma200=tampilkan_ma200,
        tampilkan_bollinger=tampilkan_bollinger,
        tampilkan_rsi=tampilkan_rsi,
        tampilkan_macd=tampilkan_macd,
        tampilkan_atr=tampilkan_atr,
        tampilkan_volatilitas=tampilkan_volatilitas,
        tinggi=tinggi,
        tanggal_dari=tanggal_dari,
        tanggal_sampai=tanggal_sampai,
    ).bangun()


def buat_grafik_komparasi(
    dict_data: dict,
    judul: str = "Perbandingan Saham",
    *,
    tinggi: int = 500,
    tanggal_dari: str = None,
    tanggal_sampai: str = None,
) -> go.Figure:
    return GrafikKomparasi(
        dict_data, judul,
        tinggi=tinggi,
        tanggal_dari=tanggal_dari,
        tanggal_sampai=tanggal_sampai,
    ).bangun()

def load_stock_data(tickers, period: str = "1y", periode: str = None,
                    verbose: bool = True) -> dict:
    return muat_data_saham(tickers, periode=periode or period, verbose=verbose)


plot_candlestick            = buat_grafik_candlestick
plot_candlestick_comparison = buat_grafik_komparasi
