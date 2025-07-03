
import streamlit as st
import sqlite3
from datetime import date

def show():
    st.title("Painel do Dia")

    conn = sqlite3.connect("data/banco.db")
    cursor = conn.cursor()

    especialidades = [row[0] for row in cursor.execute("SELECT DISTINCT especialidade FROM medicos")]
    filtro = st.selectbox("Filtrar por especialidade", ["Todas"] + especialidades)

    data_hoje = str(date.today())
    if filtro == "Todas":
        consultas = cursor.execute("""
            SELECT c.data, c.hora, p.nome, m.nome, m.especialidade, c.pagamento, c.status
            FROM consultas c
            JOIN pacientes p ON c.paciente_id = p.id
            JOIN medicos m ON c.medico_id = m.id
            WHERE c.data = ?
        """, (data_hoje,)).fetchall()
    else:
        consultas = cursor.execute("""
            SELECT c.data, c.hora, p.nome, m.nome, m.especialidade, c.pagamento, c.status
            FROM consultas c
            JOIN pacientes p ON c.paciente_id = p.id
            JOIN medicos m ON c.medico_id = m.id
            WHERE c.data = ? AND m.especialidade = ?
        """, (data_hoje, filtro)).fetchall()

    conn.close()

    if consultas:
        st.dataframe(consultas, use_container_width=True)
    else:
        st.info("Nenhuma consulta agendada para hoje.")
