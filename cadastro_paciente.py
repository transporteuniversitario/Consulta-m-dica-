
import streamlit as st
import sqlite3

def show():
    st.title("Cadastro de Paciente")
    nome = st.text_input("Nome completo")
    nascimento = st.date_input("Data de nascimento")
    responsavel = st.text_input("Nome do responsável")
    telefone = st.text_input("Telefone de contato")

    if st.button("Cadastrar Paciente"):
        if nome and telefone:
            conn = sqlite3.connect("data/banco.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pacientes (nome, nascimento, responsavel, telefone) VALUES (?, ?, ?, ?)",
                           (nome, nascimento, responsavel, telefone))
            conn.commit()
            conn.close()
            st.success("Paciente cadastrado com sucesso!")
