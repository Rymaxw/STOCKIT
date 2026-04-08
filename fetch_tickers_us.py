import yfinance as yf
import json
import time
from datetime import datetime
import os

TOP30_US = [
    # --- The Magnificent Seven & Tech Giants ---
    'AAPL',   # Apple Inc.
    'MSFT',   # Microsoft Corp.
    'GOOGL',  # Alphabet Inc. (Class A)
    'AMZN',   # Amazon.com Inc.
    'NVDA',   # NVIDIA Corp.
    'META',   # Meta Platforms Inc.
    'TSLA',   # Tesla Inc.

    # --- Semiconductors & Hardware ---
    'AVGO',   # Broadcom Inc.
    'AMD',    # Advanced Micro Devices
    'ORCL',   # Oracle Corp.

    # --- Financials ---
    'BRK-B',  # Berkshire Hathaway
    'JPM',    # JPMorgan Chase & Co.
    'V',      # Visa Inc.
    'MA',     # Mastercard Inc.
    'BAC',    # Bank of America Corp.

    # --- Healthcare & Pharma ---
    'LLY',    # Eli Lilly and Co.
    'UNH',    # UnitedHealth Group
    'JNJ',    # Johnson & Johnson
    'MRK',    # Merck & Co.
    'ABBV',   # AbbVie Inc.

    # --- Retail & Consumer Goods ---
    'WMT',    # Walmart Inc.
    'PG',     # Procter & Gamble
    'COST',   # Costco Wholesale
    'HD',     # Home Depot
    'KO',     # Coca-Cola Co.
    'PEP',    # PepsiCo Inc.

    # --- Energy, Entertainment & Software ---
    'CVX',    # Chevron Corp.
    'XOM',    # Exxon Mobil Corp.
    'CRM',    # Salesforce Inc.
    'NFLX',   # Netflix Inc.
]


def validate_ticker(symbol):
    try:
        data = yf.download(symbol, period="10y", progress=False, auto_adjust=True)
        available = not data.empty
        return {
            "ticker":     symbol,
            "yf_symbol":  symbol,
            "available":  available,
            "rows_found": len(data),
            "note":       "OK" if available else "No data returned",
        }
    except Exception as e:
        return {
            "ticker":     symbol,
            "yf_symbol":  symbol,
            "available":  False,
            "rows_found": 0,
            "note":       str(e),
        }


def build_tickers_us_json():
    results = []
    failed  = []

    print(f"Memvalidasi {len(TOP30_US)} ticker US Stock...\n")

    for symbol in TOP30_US:
        result = validate_ticker(symbol)
        results.append(result)

        status = "✓" if result["available"] else "✗"
        print(f"  [{status}] {symbol:<8} — {result['rows_found']} baris ({result['note']})")

        if not result["available"]:
            failed.append(symbol)

        time.sleep(0.3)

    output = {
        "meta": {
            "index":        "US_TOP30",
            "generated_at": datetime.now().isoformat(),
            "total":        len(results),
            "valid":        len(results) - len(failed),
            "invalid":      len(failed),
        },
        "tickers": results,
    }

    os.makedirs("data", exist_ok=True)
    with open("data/tickers_us.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'─'*40}")
    print(f"  Valid   : {output['meta']['valid']} ticker")
    print(f"  Invalid : {output['meta']['invalid']} ticker")
    if failed:
        print(f"  Gagal   : {', '.join(failed)}")
    print(f"  File    : data/tickers_us.json")


build_tickers_us_json()
