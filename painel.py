
import streamlit as st
import pandas as pd
import os
from datetime import date

CONSULTAS_PATH = "data/consultas.csv"

def show():
    st.title("Painel do Dia")

    if not os.path.exists(CONSULTAS_PATH):
        st.warning("Nenhuma consulta agendada.")
        return

    df = pd.read_csv(CONSULTAS_PATH)
    hoje = str(date.today())
    agendamentos_hoje = df[df["Data"] == hoje]

    if agendamentos_hoje.empty:
        st.info("Nenhuma consulta para hoje.")
    else:
        st.dataframe(agendamentos_hoje)
