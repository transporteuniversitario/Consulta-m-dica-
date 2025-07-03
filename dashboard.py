import streamlit as st
import sqlite3
from datetime import date
import pandas as pd

def dashboard():
    st.title("📊 Dashboard")

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT data, status FROM agendamentos")
    agendamentos = cursor.fetchall()

    if not agendamentos:
        st.info("Nenhum agendamento cadastrado ainda.")
        conn.close()
        return

    # Criar DataFrame
    df = pd.DataFrame(agendamentos, columns=["data", "status"])

    # Contagem por status
    status_counts = df["status"].value_counts()

    st.subheader("Status dos Agendamentos")
    st.bar_chart(status_counts)

    # Agendamentos por data (últimos 30 dias)
    df["data"] = pd.to_datetime(df["data"])
    ult_30_dias = date.today() - pd.Timedelta(days=30)
    df_ult_30 = df[df["data"] >= pd.Timestamp(ult_30_dias)]

    contagem_data = df_ult_30.groupby("data").size()

    st.subheader("Agendamentos nos últimos 30 dias")
    st.line_chart(contagem_data)

    conn.close()
