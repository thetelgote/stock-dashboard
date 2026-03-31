from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fetch_data import get_stock_data
from utils import add_metrics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

companies = {
    "INFY": "INFY.NS",
    "TCS": "TCS.NS",
    "RELIANCE": "RELIANCE.NS"
}

@app.get("/companies")
def get_companies():
    return list(companies.keys())

@app.get("/data/{symbol}")
def get_data(symbol: str):
    ticker = companies.get(symbol.upper())
    if not ticker:
        return {"error": "Invalid symbol"}

    df = get_stock_data(ticker, "30d")
    df = add_metrics(df)
    df = df.fillna(0)

    return df.to_dict(orient="records")

@app.get("/summary/{symbol}")
def get_summary(symbol: str):
    ticker = companies.get(symbol.upper())
    if not ticker:
        return {"error": "Invalid symbol"}

    df = get_stock_data(ticker, "365d")
    df = df.fillna(0)

    return {
        "52_week_high": float(df["High"].max()),
        "52_week_low": float(df["Low"].min()),
        "average_close": float(df["Close"].mean())
    }

@app.get("/compare")
def compare(symbol1: str, symbol2: str):
    t1 = companies.get(symbol1.upper())
    t2 = companies.get(symbol2.upper())

    if not t1 or not t2:
        return {"error": "Invalid symbols"}

    df1 = get_stock_data(t1, "30d")
    df2 = get_stock_data(t2, "30d")

    df1 = df1.fillna(0)
    df2 = df2.fillna(0)

    return {
        symbol1: df1["Close"].tolist(),
        symbol2: df2["Close"].tolist()
    }