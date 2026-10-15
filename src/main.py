import json
import yaml
import yfinance as yf

from indicators import add_indicators
from trend_analysis import get_trend

from market_structure import (
    get_phase,
    detect_bos,
    detect_choch
)

from liquidity_analysis import (
    detect_liquidity_sweep,
    detect_fvg,
    detect_order_block
)

from signal_generator import generate_signal


print("ANALISIS FOREX")

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

pairs = config["pairs"]

results = []

for pair in pairs:

    print()
    print("=" * 50)

    print("PAR:", pair)

    data = yf.download(
        pair,
        period="1y",
        interval="1d"
    )

    if hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    data = add_indicators(data)

    trend = get_trend(data)

    phase = get_phase(data)

    bos = detect_bos(data)

    choch = detect_choch(data)

    liquidity = detect_liquidity_sweep(data)

    fvg = detect_fvg(data)

    order_block = detect_order_block(data)

    signal, confidence = generate_signal(
        trend,
        phase,
        bos,
        choch
    )

    price = float(data["Close"].iloc[-1])
    
    tenkan = float(data["TENKAN"].iloc[-1])

    kijun = float(data["KIJUN"].iloc[-1])

    senkou_a = float(data["SENKOU_A"].iloc[-1])

    senkou_b = float(data["SENKOU_B"].iloc[-1])

    cloud_top = max(senkou_a, senkou_b)

    cloud_bottom = min(senkou_a, senkou_b)
    

    atr = float(data["ATR"].iloc[-1])

    if signal == "COMPRAR":

        entry = price - (atr * 0.5)

        sl = price - (atr * 1.5)

        tp = entry + ((entry - sl) * 2)

    elif signal == "VENDER":

        entry = price + (atr * 0.5)

        sl = price + (atr * 1.5)

        tp = entry - ((sl - entry) * 2)

    else:

        entry = price

        sl = None

        tp = None

    rr = 2.0

    if liquidity:
        confidence += 5

    if fvg:
        confidence += 5

    if order_block:
        confidence += 5

    if signal == "COMPRAR":

        if price > cloud_top:

            confidence += 5

        if tenkan > kijun:

            confidence += 5


    if signal == "VENDER":

        if price < cloud_bottom:

            confidence += 5

        if tenkan < kijun:

            confidence += 5

    confidence = min(confidence, 95)

    results.append({
        "pair": pair,
        "signal": signal,
        "confidence": confidence,

        "trend": trend,
        "phase": phase,

        "bos": str(bos),
        "choch": str(choch),

        "liquidity": str(liquidity),
        "fvg": str(fvg),
        "order_block": str(order_block),

        "price": round(price, 5),

        "entry": round(entry, 5),

        "sl": round(sl, 5) if sl is not None else None,

        "tp": round(tp, 5) if tp is not None else None,

        "rr": rr
    })

    print("TENDENCIA:", trend)
    print("FASE:", phase)
    print("BOS:", bos)
    print("CHOCH:", choch)
    print("LIQUIDITY:", liquidity)
    print("FVG:", fvg)
    print("ORDER BLOCK:", order_block)
    print("SEÑAL:", signal)
    print("FIABILIDAD:", str(confidence) + "%")

    print("PRECIO:", round(price, 5))
    print("ENTRADA:", round(entry, 5))

    if sl is not None:
        print("SL:", round(sl, 5))

    if tp is not None:
        print("TP:", round(tp, 5))

    print("RR:", rr)

    print("=" * 50)

results = sorted(
    results,
    key=lambda x: x["confidence"],
    reverse=True
)

compras = [
    x for x in results
    if x["signal"] == "COMPRAR"
]

ventas = [
    x for x in results
    if x["signal"] == "VENDER"
]

compras = compras[:10]

ventas = ventas[:10]

print()
print("=" * 50)
print("TOP 10 COMPRAS")
print("=" * 50)

for i, item in enumerate(compras, start=1):

    print(
        f"{i}. "
        f"{item['pair']} | "
        f"{item['confidence']}%"
    )

print()
print("=" * 50)
print("TOP 10 VENTAS")
print("=" * 50)

for i, item in enumerate(ventas, start=1):

    print(
        f"{i}. "
        f"{item['pair']} | "
        f"{item['confidence']}%"
    )

data_web = {
    "compras": compras,
    "ventas": ventas
}

with open("results.json", "w") as file:
    json.dump(
        data_web,
        file,
        indent=4
    )
