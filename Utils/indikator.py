import numpy as np
import pandas as pd


class PenghitungIndikator:

    @staticmethod
    def hitung_rerata_bergerak(df: pd.DataFrame, jendela: int, kolom: str = 'Close') -> pd.Series:
        return df[kolom].rolling(window=jendela, min_periods=1).mean()

    @staticmethod
    def hitung_rsi(df: pd.DataFrame, jendela: int = 14, kolom: str = 'Close') -> pd.Series:
        perubahan = df[kolom].diff()
        kenaikan = perubahan.clip(lower=0)
        penurunan = -perubahan.clip(upper=0)

        rerata_kenaikan = kenaikan.ewm(com=jendela - 1, adjust=False).mean()
        rerata_penurunan = penurunan.ewm(com=jendela - 1, adjust=False).mean()

        # Hindari pembagian dengan nol
        rs = rerata_kenaikan / rerata_penurunan.replace(0, np.nan)
        rs = rs.fillna(0)
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def hitung_macd(
        df: pd.DataFrame,
        jendela_cepat: int = 12,
        jendela_lambat: int = 26,
        jendela_sinyal: int = 9,
        kolom: str = 'Close'
    ) -> pd.DataFrame:
        ema_cepat = df[kolom].ewm(span=jendela_cepat, adjust=False).mean()
        ema_lambat = df[kolom].ewm(span=jendela_lambat, adjust=False).mean()
        
        garis_macd = ema_cepat - ema_lambat
        garis_sinyal = garis_macd.ewm(span=jendela_sinyal, adjust=False).mean()
        histogram_macd = garis_macd - garis_sinyal

        return pd.DataFrame({
            'MACD_Garis': garis_macd,
            'MACD_Sinyal': garis_sinyal,
            'MACD_Histogram': histogram_macd
        }, index=df.index)

    @staticmethod
    def hitung_pita_bollinger(
        df: pd.DataFrame,
        jendela: int = 20,
        deviasi: float = 2.0,
        kolom: str = 'Close'
    ) -> pd.DataFrame:
        rerata = df[kolom].rolling(window=jendela, min_periods=1).mean()
        deviasi_std = df[kolom].rolling(window=jendela, min_periods=2).std().fillna(0)

        pita_atas = rerata + (deviasi * deviasi_std)
        pita_bawah = rerata - (deviasi * deviasi_std)

        return pd.DataFrame({
            'Bollinger_Atas': pita_atas,
            'Bollinger_Tengah': rerata,
            'Bollinger_Bawah': pita_bawah
        }, index=df.index)

    @staticmethod
    def hitung_atr(df: pd.DataFrame, jendela: int = 14) -> pd.Series:
        close_sebelumnya = df['Close'].shift(1)
        tr1 = df['High'] - df['Low']
        tr2 = (df['High'] - close_sebelumnya).abs()
        tr3 = (df['Low'] - close_sebelumnya).abs()

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.ewm(alpha=1/jendela, adjust=False).mean()
        return atr

    @staticmethod
    def hitung_volatilitas_bergulir(
        df: pd.DataFrame,
        jendela: int = 30,
        kolom: str = 'Close',
        frekuensi: str = 'harian'
    ) -> pd.Series:
        log_return = np.log(df[kolom] / df[kolom].shift(1))
        
        peta_pengali = {
            'harian': np.sqrt(252),
            'mingguan': np.sqrt(52),
            'bulanan': np.sqrt(12),
            'tahunan': 1.0
        }
        pengali = peta_pengali.get(frekuensi.lower(), 1.0)
        
        # Jika data terlalu sedikit untuk jendela yang diminta, sesuaikan jendela agar tidak semuanya NaN
        jendela_aktual = min(len(df), jendela)
        if len(df) < 2:
            return pd.Series(np.nan, index=df.index)
            
        volatilitas = log_return.rolling(window=jendela_aktual, min_periods=2).std().fillna(0) * pengali
        return volatilitas
