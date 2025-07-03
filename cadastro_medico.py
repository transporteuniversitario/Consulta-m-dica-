
import streamlit as st
import pandas as pd
import os

DATA_PATH = "data/medicos.csv"

def show():
    st.title("Cadastro de Médico")
    nome = st.text_input("Nome do médico")
    especialidade = st.text_input("Especialidade")
    dias_atendimento = st.text_input("Dias de atendimento (ex: Segunda, Quarta)")

    if st.button("Cadastrar Médico"):
        if nome and especialidade and dias_atendimento:
            novo = pd.DataFrame([[nome, especialidade, dias_atendimento]],
                                columns=["Nome", "Especialidade", "Dias"])
            if os.path.exists(DATA_PATH):
                df = pd.read_csv(DATA_PATH)
                df = pd.concat([df, novo], ignore_index=True)
            else:
                df = novo
            df.to_csv(DATA_PATH, index=False)
            st.success("Médico cadastrado com sucesso!")
