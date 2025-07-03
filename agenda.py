
import streamlit as st
import sqlite3
import webbrowser

def show():
    st.title("Agendamento de Consultas")

    conn = sqlite3.connect("data/banco.db")
    cursor = conn.cursor()

    pacientes = cursor.execute("SELECT id, nome FROM pacientes").fetchall()
    medicos = cursor.execute("SELECT id, nome FROM medicos").fetchall()

    paciente = st.selectbox("Paciente", pacientes, format_func=lambda x: x[1])
    medico = st.selectbox("Médico", medicos, format_func=lambda x: x[1])
    data = st.date_input("Data da consulta")
    hora = st.time_input("Hora")
    forma_pagamento = st.text_input("Forma de pagamento")
    status = st.selectbox("Status", ["Agendado", "Confirmado", "Concluído", "Faltou"])

    if st.button("Agendar"):
        cursor.execute("INSERT INTO consultas (paciente_id, medico_id, data, hora, pagamento, status) VALUES (?, ?, ?, ?, ?, ?)",
                       (paciente[0], medico[0], data, hora.strftime("%H:%M"), forma_pagamento, status))
        conn.commit()

        telefone = cursor.execute("SELECT telefone FROM pacientes WHERE id=?", (paciente[0],)).fetchone()[0]
        mensagem = f"Olá, sua consulta foi agendada para {data} às {hora.strftime('%H:%M')} com {medico[1]}."
        link = f"https://wa.me/55{telefone}?text={mensagem.replace(' ', '%20')}"
        st.success("Consulta agendada com sucesso!")
        st.markdown(f"[Enviar confirmação via WhatsApp]({link})", unsafe_allow_html=True)

    conn.close()
