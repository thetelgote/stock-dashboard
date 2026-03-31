import yfinance as yf
import pandas as pd

def get_stock_data(symbol="INFY.NS", period="60d"):
    stock = yf.Ticker(symbol)
    df = stock.history(period=period)

    df.reset_index(inplace=True)
    df.dropna(inplace=True)

    return df