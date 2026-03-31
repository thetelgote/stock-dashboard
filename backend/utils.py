def add_metrics(df):
    df['Daily Return'] = (df['Close'] - df['Open']) / df['Open']
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    df['Volatility'] = df['Close'].rolling(window=7).std()
    return df