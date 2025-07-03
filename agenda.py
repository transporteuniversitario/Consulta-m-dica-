
import streamlit as st
import pandas as pd
import os

MEDICOS_PATH = "data/medicos.csv"
PACIENTES_PATH = "data/pacientes.csv"
CONSULTAS_PATH = "data/consultas.csv"

def show():
    st.title("Agendamento de Consultas")

    if not os.path.exists(MEDICOS_PATH) or not os.path.exists(PACIENTES_PATH):
        st.warning("Cadastre médicos e pacientes primeiro.")
        return

    medicos = pd.read_csv(MEDICOS_PATH)
    pacientes = pd.read_csv(PACIENTES_PATH)

    paciente = st.selectbox("Paciente", pacientes["Nome"])
    medico = st.selectbox("Médico", medicos["Nome"])
    data = st.date_input("Data da consulta")
    hora = st.time_input("Hora")
    forma_pagamento = st.text_input("Forma de pagamento")
    status = st.selectbox("Status", ["Agendado", "Confirmado", "Concluído", "Faltou"])

    if st.button("Agendar"):
        novo = pd.DataFrame([[paciente, medico, data, hora, forma_pagamento, status]],
                            columns=["Paciente", "Médico", "Data", "Hora", "Pagamento", "Status"])
        if os.path.exists(CONSULTAS_PATH):
            df = pd.read_csv(CONSULTAS_PATH)
            df = pd.concat([df, novo], ignore_index=True)
        else:
            df = novo
        df.to_csv(CONSULTAS_PATH, index=False)
        st.success("Consulta agendada com sucesso!")
