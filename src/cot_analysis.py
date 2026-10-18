def get_cot_bias(pair):

    cot_data = {

        "EURUSD=X": "BAJISTA",
        "GBPUSD=X": "ALCISTA",
        "USDCHF=X": "ALCISTA",
        "USDJPY=X": "ALCISTA",
        "USDCAD=X": "ALCISTA"

    }

    return cot_data.get(
        pair,
        "NEUTRAL"
    )