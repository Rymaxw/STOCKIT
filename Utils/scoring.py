import pandas as pd
import numpy as np
import os
import glob

def load_all_cleaned_data(processed_dir='data/processed'):
    """
    Fungsi bantuan untuk memuat semua data parquet yang sudah dibersihkan.
    Mengembalikan DataFrame gabungan dengan kolom 'Ticker'.
    """
    all_files = glob.glob(os.path.join(processed_dir, "*_clean.parquet"))
    df_list = []
    
    for file in all_files:
        filename = os.path.basename(file)
        ticker = filename.split('_clean.parquet')[0]
        
        try:
            df = pd.read_parquet(file)
            df['Ticker'] = ticker
            df_list.append(df)
        except Exception as e:
            print(f"Gagal memuat {filename}: {e}")
            
    if not df_list:
        return pd.DataFrame()
        
    return pd.concat(df_list)

def calculate_score(df):
    """
    Fungsi untuk menghitung skor dan meranking saham.
    Menerima DataFrame gabungan yang memiliki kolom 'Ticker'.
    
    Metrik:
    - Return 30 Hari (40%): (Close_hari_ini - Close_30_hari_lalu) / Close_30_hari_lalu
    - Sharpe Ratio (40%): (Mean Daily Return / Std Daily Return) * sqrt(252) (Asumsi risk free = 0)
    - Volatilitas (20%): Std Daily Return * sqrt(252) (Semakin rendah semakin baik)
    """
    # Handle apabila input berupa dictionary (untuk fleksibilitas)
    if isinstance(df, dict):
        df_list = []
        for ticker, data in df.items():
            temp = data.copy()
            temp['Ticker'] = ticker
            df_list.append(temp)
        df = pd.concat(df_list)
        
    if 'Ticker' not in df.columns:
        raise ValueError("DataFrame harus memiliki kolom 'Ticker' untuk membedakan tiap saham.")
        
    results = []
    
    for ticker, group in df.groupby('Ticker'):
        group = group.sort_index()
        
        if len(group) < 2:
            continue
            
        group['Daily_Return'] = group['Close'].pct_change()
        lookback = min(30, len(group) - 1)
        close_today = group['Close'].iloc[-1]
        close_past = group['Close'].iloc[-(lookback + 1)]
        return_30d = (close_today - close_past) / close_past
        
        mean_return = group['Daily_Return'].mean()
        std_return = group['Daily_Return'].std()
        
        if pd.isna(std_return) or std_return == 0:
            sharpe_ratio = 0
            volatility = 0
        else:
            sharpe_ratio = (mean_return / std_return) * np.sqrt(252)
            volatility = std_return * np.sqrt(252)
            
        results.append({
            'Ticker': ticker,
            'Return_30D': return_30d,
            'Sharpe_Ratio': sharpe_ratio,
            'Volatility': volatility
        })
        
    results_df = pd.DataFrame(results)
    
    if results_df.empty:
        return results_df
        
    for col in ['Return_30D', 'Sharpe_Ratio']:
        min_val = results_df[col].min()
        max_val = results_df[col].max()
        if max_val != min_val:
            results_df[col + '_Norm'] = (results_df[col] - min_val) / (max_val - min_val)
        else:
            results_df[col + '_Norm'] = 0.5
            
    # Untuk Volatilitas: semakin rendah semakin baik (Inverse Min-Max: 1 - Normalized)
    min_vol = results_df['Volatility'].min()
    max_vol = results_df['Volatility'].max()
    if max_vol != min_vol:
        results_df['Volatility_Norm'] = 1 - ((results_df['Volatility'] - min_vol) / (max_vol - min_vol))
    else:
        results_df['Volatility_Norm'] = 0.5
        
    results_df['Final_Score'] = (
        results_df['Return_30D_Norm'] * 0.40 +
        results_df['Sharpe_Ratio_Norm'] * 0.40 +
        results_df['Volatility_Norm'] * 0.20
    )
    
    results_df = results_df.sort_values(by='Final_Score', ascending=False).reset_index(drop=True)

    return results_df.head(5)

if __name__ == "__main__":
    print("Memuat data...")
    df_all = load_all_cleaned_data('../data/processed')
    if df_all.empty:
        df_all = load_all_cleaned_data('data/processed')
        
    if not df_all.empty:
        print("Data berhasil dimuat. Menghitung skor...")
        top5 = calculate_score(df_all)
        print("\n=== TOP 5 SAHAM TERBAIK ===")
        print(top5[['Ticker', 'Return_30D', 'Sharpe_Ratio', 'Volatility', 'Final_Score']])
    else:
        print("Tidak ada data yang dimuat.")
