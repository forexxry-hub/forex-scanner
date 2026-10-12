def get_phase(df):

    close = df["Close"].iloc[-1]

    ema20 = df["EMA20"].iloc[-1]

    ema50 = df["EMA50"].iloc[-1]

    if close > ema20 and ema20 > ema50:
        return "IMPULSO"

    if close < ema20 and ema20 > ema50:
        return "RETROCESO"

    return "CORRECCION"


def detect_bos(df):

    previous_high = df["High"].iloc[-20:-1].max()

    current_close = df["Close"].iloc[-1]

    return current_close > previous_high


def detect_choch(df):

    previous_low = df["Low"].iloc[-20:-1].min()

    current_close = df["Close"].iloc[-1]

    return current_close < previous_low
