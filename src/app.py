import json
import streamlit as st
import subprocess

st.set_page_config(
    page_title="Forex Scanner",
    layout="wide"
)

USUARIO = "mdrl"
PASSWORD = "1917"

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("Acceso privado")

    usuario = st.text_input("Usuario")

    password = st.text_input(
        "Contraseña",
        type="password"
    )

    if st.button("Entrar"):

        if (
            usuario == USUARIO
            and
            password == PASSWORD
        ):

            st.session_state.login = True
            st.rerun()

        else:

            st.error(
                "Usuario o contraseña incorrectos"
            )

else:

    st.title("Forex Scanner")

    if st.button("🔄 Actualizar análisis"):

        subprocess.run(
            ["python", "src/main.py"]
        )

        st.success(
            "Análisis actualizado"
        )

    with open("results.json", "r") as file:
        data = json.load(file)

    compras = data["compras"]

    ventas = data["ventas"]

    st.header("TOP 10 COMPRAS")

    for item in compras:

        st.success(
            f"""
PAR: {item['pair']}

SEÑAL: {item['signal']}

CONFIANZA: {item['confidence']}%

PRECIO ACTUAL: {item['price']}

ENTRADA: {item['entry']}

STOP LOSS: {item['sl']}

TAKE PROFIT: {item['tp']}

R:R = {item['rr']}
"""
        )

    st.header("TOP 10 VENTAS")

    for item in ventas:

        st.error(
            f"""
PAR: {item['pair']}

SEÑAL: {item['signal']}

CONFIANZA: {item['confidence']}%

PRECIO ACTUAL: {item['price']}

ENTRADA: {item['entry']}

STOP LOSS: {item['sl']}

TAKE PROFIT: {item['tp']}

R:R = {item['rr']}
"""
        )
