import yaml
import yfinance as yf
import json

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

    if liquidity:
        confidence += 5

    if fvg:
        confidence += 5

    if order_block:
        confidence += 5

    confidence = min(confidence, 95)

    results.append({
        "pair": pair,
        "signal": signal,
        "confidence": confidence
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

    print("=" * 50)

print()
print("=" * 50)
print("TOP OPORTUNIDADES")
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

compras = compras[:5]

ventas = ventas[:5]

print()
print("=" * 50)
print("TOP 5 COMPRAS")
print("=" * 50)

for i, item in enumerate(compras, start=1):

    print(
        f"{i}. "
        f"{item['pair']} | "
        f"{item['confidence']}%"
    )

print()
print("=" * 50)
print("TOP 5 VENTAS")
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