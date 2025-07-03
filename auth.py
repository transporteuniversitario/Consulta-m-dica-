
import streamlit as st

# Login fixo para exemplo
USERS = {"admin": "123"}

def login():
    st.title("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if usuario in USERS and USERS[usuario] == senha:
            st.session_state.logged_in = True
        else:
            st.error("Usuário ou senha inválidos.")
