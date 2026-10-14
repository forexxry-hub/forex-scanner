import ta


def add_indicators(df):

    close = df["Close"].squeeze()

    high = df["High"].squeeze()

    low = df["Low"].squeeze()

    df["EMA20"] = ta.trend.ema_indicator(
        close,
        window=20
    )

    df["EMA50"] = ta.trend.ema_indicator(
        close,
        window=50
    )

    df["EMA200"] = ta.trend.ema_indicator(
        close,
        window=200
    )

    df["RSI"] = ta.momentum.rsi(
        close,
        window=14
    )

    df["MACD"] = ta.trend.macd(
        close
    )

    df["MACD_SIGNAL"] = ta.trend.macd_signal(
        close
    )

    df["ATR"] = ta.volatility.average_true_range(
        high,
        low,
        close
    )

    ichimoku = ta.trend.IchimokuIndicator(
        high=high,
        low=low
    )

    df["TENKAN"] = ichimoku.ichimoku_conversion_line()

    df["KIJUN"] = ichimoku.ichimoku_base_line()

    df["SENKOU_A"] = ichimoku.ichimoku_a()

    df["SENKOU_B"] = ichimoku.ichimoku_b()


    return df
