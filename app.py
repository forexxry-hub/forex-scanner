import streamlit as st
import yaml

st.set_page_config(
    page_title="Forex Technical Analyzer",
    page_icon="📈",
    layout="wide"
)

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

pairs = config["pairs"]

st.title("📈 Forex Technical Analyzer")

st.markdown("---")

st.subheader("TOP OPORTUNIDADES")

st.success("1. XAUUSD | COMPRAR | 93%")
st.success("2. EURUSD | COMPRAR | 90%")
st.error("3. GBPJPY | VENDER | 88%")
st.success("4. EURJPY | COMPRAR | 86%")
st.success("5. AUDUSD | COMPRAR | 84%")

st.markdown("---")

par = st.selectbox(
    "Selecciona un activo",
    pairs
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.metric("ESTADO", "ALCISTA")
    st.metric("FASE", "RETROCESO")

with col2:
    st.metric("ACCION", "COMPRAR")
    st.metric("FIABILIDAD", "89%")

st.markdown("---")

st.write("Activo seleccionado:", par)

st.write("BOS: ✅")

st.write("CHOCH: ❌")

st.write("LIQUIDITY SWEEP: ✅")

st.write("FVG: ✅")

st.write("ORDER BLOCK: ✅")
