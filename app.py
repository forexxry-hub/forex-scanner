import streamlit as st
import pandas as pd
import yfinance as yf

# Configuración visual para pantallas móviles
st.set_page_config(page_title="Forex H4 Scanner", page_icon="📈", layout="centered")

st.title("📈 Escáner Cuantitativo Forex H4")
st.caption("Filtro técnico automático: SMA 200 + RSI (14)")

MIS_PARES = [
    "audcad", "audchf", "audjpy", "audnzd", "audusd", 
    "cadchf", "cadjpy", "chfjpy", "euraud", "eurcad", 
    "eurusd", "nzdusd", "eurchf", "eurnzd", "gbpusd", 
    "nzdcad", "usdjpy", "eurgbp", "usdchf", "eurjpy", 
    "gbpaud", "gbpcad", "gbpchf", "gbpjpy", "gbpnzd", 
    "nzdchf", "nzdjpy", "usdcad", "xauusd"
]

def calcular_sma(serie, window=200):
    return serie.rolling(window=window).mean()

def calcular_rsi(serie, window=14):
    delta = serie.diff()
    ganancia = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    perdida = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = ganancia / perdida
    return 100 - (100 / (1 + rs))

if st.button("🚀 Escanear Oportunidades Ahora", type="primary", use_container_width=True):
    with st.spinner("Analizando 29 activos en vivo..."):
        resultados = []
        
        for p in MIS_PARES:
            p_clean = p.strip().lower()
            ticker = "GC=F" if p_clean == "xauusd" else f"{p_clean.upper()}=X"
            
            try:
                df = yf.download(ticker, period="60d", interval="1h", progress=False)
                if df is None or df.empty or len(df) < 50:
                    df = yf.download(ticker, period="1y", interval="1d", progress=False)
                
                if df is None or df.empty:
                    continue
                
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                df = df.loc[:, ~df.columns.duplicated()]
                
                if "Close" not in df.columns:
                    continue
                    
                close_series = df["Close"].squeeze()
                if len(close_series) > 250:
                    close_series = close_series.resample("4h").last().dropna()
                
                if len(close_series) < 200:
                    continue
                    
                sma200 = float(calcular_sma(close_series, 200).iloc[-1])
                rsi = float(calcular_rsi(close_series, 14).iloc[-1])
                precio = float(close_series.iloc[-1])
                
                if pd.isna(sma200) or pd.isna(rsi):
                    continue
                    
                tendencia = "ALCISTA" if precio > sma200 else "BAJISTA"
                
                # Puntuación por extremidad de RSI a favor de tendencia
                score = 0
                if tendencia == "BAJISTA" and rsi < 35:
                    score = 35 - rsi
                elif tendencia == "ALCISTA" and rsi > 65:
                    score = rsi - 65
                
                senal = "🟢 COMPRA" if tendencia == "ALCISTA" else "🔴 VENTA"

                resultados.append({
                    "Par": p.upper(),
                    "Señal": senal,
                    "Precio": round(precio, 5),
                    "RSI (14)": round(rsi, 2),
                    "SMA 200": round(sma200, 5),
                    "Tendencia": tendencia,
                    "Score": score
                })
            except Exception:
                continue

        if resultados:
            df_res = pd.DataFrame(resultados)
            df_res = df_res.sort_values(by="Score", ascending=False)
            
            st.success(f"¡Análisis completado! {len(df_res)} activos analizados.")
            
            st.subheader("🔥 Top 5 Mejores Oportunidades")
            top_5 = df_res.head(5)[["Par", "Señal", "Precio", "RSI (14)", "Tendencia"]]
            st.dataframe(top_5, hide_index=True, use_container_width=True)
            
            with st.expander("📋 Ver todos los activos escaneados"):
                st.dataframe(df_res[["Par", "Señal", "Precio", "RSI (14)", "SMA 200"]], hide_index=True, use_container_width=True)
        else:
            st.error("No se pudieron obtener datos del mercado en este momento.")
