import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import json
import sys

def get_nifty50_symbols():
    return [
        "ADANIPORTS.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS",
        "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS",
        "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS",
        "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
        "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS",
        "ITC.NS", "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS",
        "LT.NS", "M&M.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS", "ONGC.NS",
        "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS",
        "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS",
        "TITAN.NS", "UPL.NS", "ULTRACEMCO.NS", "WIPRO.NS"
    ]

def get_live_data(symbol):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5)
        data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
        return data
    except Exception as e:
        print(f"Error downloading data for {symbol}: {str(e)}", file=sys.stderr)
        return None

def get_stock_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        return stock.info
    except Exception as e:
        print(f"Error fetching info for {symbol}: {str(e)}", file=sys.stderr)
        return {}

def format_data(symbol, data, info):
    if data is None or data.empty:
        return None

    latest_data = data.iloc[-1]
    prev_data = data.iloc[-2] if len(data) > 1 else latest_data

    return {
        "Symbol": symbol.replace(".NS", ""),
        "Current Price": latest_data["Close"],
        "Open": latest_data["Open"],
        "High": latest_data["High"],
        "Low": latest_data["Low"],
        "Previous Close": prev_data["Close"],
        "Change": latest_data["Close"] - prev_data["Close"],
        "Change %": ((latest_data["Close"] - prev_data["Close"]) / prev_data["Close"]) * 100,
        "Volume": latest_data["Volume"],
        "Day's Range": f"{latest_data['Low']:.2f} - {latest_data['High']:.2f}",
        "52 Week Range": f"{info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}",
        "Market Cap": info.get('marketCap', 'N/A'),
        "P/E Ratio": info.get('trailingPE', 'N/A'),
        "EPS": info.get('trailingEps', 'N/A'),
        "Dividend Yield": info.get('dividendYield', 'N/A'),
    }

def get_historical_data(symbol):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5)
        data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
        return data.to_dict(orient='records')
    except Exception as e:
        print(f"Error downloading historical data for {symbol}: {str(e)}", file=sys.stderr)
        return []

if __name__ == "__main__":
    symbols = get_nifty50_symbols()

    if len(sys.argv) > 1 and sys.argv[1] == 'historical':
        historical_data = {}
        for symbol in symbols:
            historical_data[symbol] = get_historical_data(symbol)
        print(json.dumps(historical_data), flush=True)
        sys.stdout.flush()
    else:
        while True:
            try:
                formatted_data = []
                for symbol in symbols:
                    live_data = get_live_data(symbol)
                    stock_info = get_stock_info(symbol)
                    stock_data = format_data(symbol, live_data, stock_info)
                    if stock_data:
                        formatted_data.append(stock_data)
                
                print(json.dumps(formatted_data), flush=True)
                sys.stdout.flush()
                time.sleep(300)
            except Exception as e:
                print(f"An error occurred: {e}", file=sys.stderr)
                time.sleep(60)