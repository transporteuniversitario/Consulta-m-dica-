
import streamlit as st
import sqlite3

def show():
    st.title("Cadastro de Médico")
    nome = st.text_input("Nome do médico")
    especialidade = st.text_input("Especialidade")
    dias_atendimento = st.text_input("Dias de atendimento (ex: Segunda, Quarta)")

    if st.button("Cadastrar Médico"):
        if nome and especialidade and dias_atendimento:
            conn = sqlite3.connect("data/banco.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO medicos (nome, especialidade, dias) VALUES (?, ?, ?)",
                           (nome, especialidade, dias_atendimento))
            conn.commit()
            conn.close()
            st.success("Médico cadastrado com sucesso!")
