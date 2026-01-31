#!/usr/bin/env python3
"""
Automatic Portfolio Tracker Price Fetcher
Fetches live stock prices and dividends, saves to JSON for web app
"""

import json
import yfinance as yf
from datetime import datetime
import time

# Portfolio stocks with proper Yahoo Finance tickers
STOCKS = {
    'PPL': 'PPL.TO',           # Pembina Pipeline
    'SHOP': 'SHOP.TO',         # Shopify
    'CSU': 'CSU.TO',           # Constellation Software
    'TOU': 'TOU.TO',           # Tourmaline Oil
    'AIF': 'AIF.TO',           # Altus Group
    'OTEX': 'OTEX',            # Open Text
    'CAE': 'CAE.TO',           # CAE Inc
    'NVDA': 'NVDA',            # NVIDIA
    'UNH': 'UNH',              # UnitedHealth
    'MSFT': 'MSFT',            # Microsoft
    'BDX': 'BDX',              # Becton Dickinson
    'ORCL': 'ORCL',            # Oracle
    'ASML': 'ASML',            # ASML Holding
    'TSM': 'TSM',              # Taiwan Semi
    'SE': 'SE',                # Sea Limited
    'LVMUY': 'LVMUY',          # LVMH ADR
    'BAESY': 'BAESY',          # BAE Systems ADR
    'DNNGY': 'DNNGY',          # Orsted ADR
}

# September 19, 2024 baseline prices (you'll need to fill these in)
BASELINE_PRICES = {
    'PPL': 54.43,
    'SHOP':211.60 ,
    'CSU': 4415.49,
    'TOU': 60.06,
    'AIF': 57.89,
    'OTEX': 50.5,
    'CAE': 38.58,
    'NVDA': 176.66,
    'UNH': 334.44,
    'MSFT': 516.96,
    'BDX': 186.03,
    'ORCL': 307.31,
    'ASML': 930.5,
    'TSM': 264.16,
    'SE': 192.76,
    'LVMUY': 120.24,
    'BAESY': 105.24,
    'DNNGY': 10.66,
}

BASELINE_DATE = '2024-09-19'

def get_stock_data(ticker, yahoo_ticker):
    """Fetch current price and dividends for a stock"""
    try:
        stock = yf.Ticker(yahoo_ticker)
        
        # Get current price
        current_data = stock.history(period='1d')
        if current_data.empty:
            print(f"Warning: No price data for {ticker}")
            return None
        
        current_price = current_data['Close'].iloc[-1]
        
        # Get dividends since baseline date
        dividends = stock.dividends
        if not dividends.empty:
            # Filter dividends after Sep 19, 2024
            dividends_since_baseline = dividends[dividends.index >= BASELINE_DATE]
            total_dividends = dividends_since_baseline.sum()
        else:
            total_dividends = 0.0
        
        return {
            'ticker': ticker,
            'yahoo_ticker': yahoo_ticker,
            'current_price': float(current_price),
            'baseline_price': BASELINE_PRICES[ticker],
            'dividends_since_baseline': float(total_dividends),
            'last_updated': datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def get_bitcoin_price():
    """Fetch Bitcoin price in CAD"""
    try:
        btc = yf.Ticker('BTC-CAD')
        current_data = btc.history(period='1d')
        
        if current_data.empty:
            print("Warning: No Bitcoin price data")
            return None
        
        current_price = current_data['Close'].iloc[-1]
        
        # Get historical price for Sep 19, 2024
        historical = btc.history(start='2024-09-18', end='2024-09-20')
        if not historical.empty:
            baseline_price = historical['Close'].iloc[0]
        else:
            baseline_price = 85000.00  # Fallback
        
        return {
            'ticker': 'BTC-CAD',
            'current_price': float(current_price),
            'baseline_price': float(baseline_price),
            'last_updated': datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"Error fetching Bitcoin: {e}")
        return None

def fetch_all_data():
    """Fetch all stock and Bitcoin data"""
    print(f"Fetching data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    data = {
        'stocks': {},
        'bitcoin': None,
        'last_updated': datetime.now().isoformat()
    }
    
    # Fetch stock data
    for ticker, yahoo_ticker in STOCKS.items():
        print(f"Fetching {ticker}...", end=' ')
        stock_data = get_stock_data(ticker, yahoo_ticker)
        if stock_data:
            data['stocks'][ticker] = stock_data
            print(f"✓ ${stock_data['current_price']:.2f}")
        else:
            print("✗ Failed")
        time.sleep(0.5)  # Be nice to the API
    
    # Fetch Bitcoin
    print("Fetching Bitcoin...", end=' ')
    btc_data = get_bitcoin_price()
    if btc_data:
        data['bitcoin'] = btc_data
        print(f"✓ ${btc_data['current_price']:.2f}")
    else:
        print("✗ Failed")
    
    return data

def save_to_json(data, filename='portfolio_data.json'):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\nData saved to {filename}")

if __name__ == '__main__':
    print("=" * 60)
    print("Portfolio Tracker - Automatic Price Fetcher")
    print("=" * 60)
    print()
    
    # Fetch and save data
    data = fetch_all_data()
    save_to_json(data)
    
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"Stocks fetched: {len(data['stocks'])}/{len(STOCKS)}")
    print(f"Bitcoin: {'✓' if data['bitcoin'] else '✗'}")
    print(f"Last updated: {data['last_updated']}")
    print("=" * 60)
