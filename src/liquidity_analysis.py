def detect_liquidity_sweep(df):

    recent_high = df["High"].iloc[-10:-1].max()

    current_high = df["High"].iloc[-1]

    return current_high > recent_high


def detect_fvg(df):

    candle_1_high = df["High"].iloc[-3]

    candle_3_low = df["Low"].iloc[-1]

    return candle_3_low > candle_1_high


def detect_order_block(df):

    recent_low = df["Low"].iloc[-10:-1].min()

    current_close = df["Close"].iloc[-1]

    return current_close <= (recent_low * 1.003)