
import streamlit as st
from utils.auth import login, check_auth
from pages import cadastro_medico, cadastro_paciente, agenda, painel

st.set_page_config(page_title="Sistema de Agendamento Médico", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Ir para", ["Cadastro Médico", "Cadastro Paciente", "Agendamentos", "Painel do Dia"])
    if page == "Cadastro Médico":
        cadastro_medico.show()
    elif page == "Cadastro Paciente":
        cadastro_paciente.show()
    elif page == "Agendamentos":
        agenda.show()
    elif page == "Painel do Dia":
        painel.show()
