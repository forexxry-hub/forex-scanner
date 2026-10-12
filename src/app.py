import json
import streamlit as st

st.set_page_config(
    page_title="Forex Scanner",
    layout="wide"
)

USUARIO = "manuel"
PASSWORD = "1234"

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

    with open("results.json", "r") as file:
        data = json.load(file)

    compras = data["compras"]

    ventas = data["ventas"]

    st.header("TOP 5 COMPRAS")

    for item in compras:

        st.success(
            f"{item['pair']} | "
            f"{item['confidence']}%"
        )

    st.header("TOP 5 VENTAS")

    for item in ventas:

        st.error(
            f"{item['pair']} | "
            f"{item['confidence']}%"
        )