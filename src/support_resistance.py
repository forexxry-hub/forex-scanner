def get_support(df):
    return df["Low"].tail(50).min()

def get_resistance(df):
    return df["High"].tail(50).max()
