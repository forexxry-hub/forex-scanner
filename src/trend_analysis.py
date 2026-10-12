def get_trend(df):

    ema20 = df["EMA20"].iloc[-1]
    ema50 = df["EMA50"].iloc[-1]
    ema200 = df["EMA200"].iloc[-1]

    if ema20 > ema50 > ema200:
        return "ALCISTA"

    if ema20 < ema50 < ema200:
        return "BAJISTA"

    return "LATERAL"
