
import streamlit as st
import pandas as pd
import os

DATA_PATH = "data/pacientes.csv"

def show():
    st.title("Cadastro de Paciente")
    nome = st.text_input("Nome completo")
    nascimento = st.date_input("Data de nascimento")
    responsavel = st.text_input("Nome do responsável")
    telefone = st.text_input("Telefone de contato")

    if st.button("Cadastrar Paciente"):
        if nome and telefone:
            novo = pd.DataFrame([[nome, nascimento, responsavel, telefone]],
                                columns=["Nome", "Nascimento", "Responsável", "Telefone"])
            if os.path.exists(DATA_PATH):
                df = pd.read_csv(DATA_PATH)
                df = pd.concat([df, novo], ignore_index=True)
            else:
                df = novo
            df.to_csv(DATA_PATH, index=False)
            st.success("Paciente cadastrado com sucesso!")
