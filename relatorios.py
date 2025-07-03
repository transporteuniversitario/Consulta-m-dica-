import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

def relatorios_mensais():
    st.title("📄 Relatórios Mensais")

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    ano_selecionado = st.selectbox("Selecione o ano", options=[2023, 2024, 2025], index=2)
    mes_selecionado = st.selectbox("Selecione o mês", options=list(range(1, 13)), index=datetime.now().month - 1)

    query = """
        SELECT 
            a.id,
            p.nome,
            m.nome,
            a.especialidade,
            a.data,
            a.hora,
            a.valor,
            a.pago,
            a.forma_pagamento,
            a.status
        FROM agendamentos a
        JOIN pacientes p ON a.paciente_id = p.id
        JOIN medicos m ON a.medico_id = m.id
        WHERE strftime('%Y', a.data) = ? AND strftime('%m', a.data) = ?
    """

    cursor.execute(query, (str(ano_selecionado), f"{mes_selecionado:02d}"))
    agendamentos = cursor.fetchall()

    if not agendamentos:
        st.info("Nenhum agendamento encontrado para o mês e ano selecionados.")
        conn.close()
        return

    df = pd.DataFrame(agendamentos, columns=[
        "ID", "Paciente", "Médico", "Especialidade", "Data", "Hora", "Valor", "Pago", "Forma de Pagamento", "Status"
    ])

    st.dataframe(df)

    # Totais
    total_valor = df["Valor"].sum()
    total_pagos = df[df["Pago"] == "Sim"]["Valor"].sum()
    st.write(f"Total de consultas no período: {len(df)}")
    st.write(f"Total recebido (pagos): R$ {total_pagos:.2f}")
    st.write(f"Valor total (considerando todos): R$ {total_valor:.2f}")

    conn.close()
