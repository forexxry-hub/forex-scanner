def get_macro_risk(pair):

    macro_events = {

        "EURUSD=X": True,
        "GBPUSD=X": False,
        "USDJPY=X": True,
        "USDCHF=X": False,
        "USDCAD=X": True

    }

    return macro_events.get(
        pair,
        False
    )