
import streamlit as st
import sqlite3

def login():
    st.title("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        conn = sqlite3.connect("data/banco.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
        result = cursor.fetchone()
        conn.close()

        if result:
            st.session_state.logged_in = True
        else:
            st.error("Usuário ou senha inválido.")

def check_auth():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.stop()
