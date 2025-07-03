import streamlit as st
import sqlite3
from datetime import date

def agendar_consulta():
    st.title("📅 Agendamento de Consulta")

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    # Selecionar paciente
    cursor.execute("SELECT id, nome FROM pacientes")
    pacientes = cursor.fetchall()
    if not pacientes:
        st.warning("Nenhum paciente cadastrado. Cadastre pacientes primeiro.")
        return
    paciente_dict = {nome: id for id, nome in pacientes}
    paciente_nome = st.selectbox("Selecione o paciente", [p[1] for p in pacientes])

    # Selecionar médico
    cursor.execute("SELECT id, nome, especialidade FROM medicos")
    medicos = cursor.fetchall()
    if not medicos:
        st.warning("Nenhum médico cadastrado. Cadastre médicos primeiro.")
        return
    medico_dict = {nome: (id, esp) for id, nome, esp in medicos}
    medico_nome = st.selectbox("Selecione o médico", [m[1] for m in medicos])

    data = st.date_input("Data da consulta", value=date.today())
    hora = st.text_input("Hora da consulta (ex: 14:30)")
    valor = st.number_input("Valor da consulta (R$)", min_value=0.0, format="%.2f")
    pago = st.selectbox("Pagamento realizado?", ["Não", "Sim"])
    forma_pagamento = st.text_input("Forma de pagamento")

    status = st.selectbox("Status do agendamento", ["Agendado", "Confirmado", "Reagendado", "Cancelado"])

    if st.button("Agendar"):
        paciente_id = paciente_dict.get(paciente_nome)
        medico_id, especialidade = medico_dict.get(medico_nome, (None, None))
        if paciente_id and medico_id and hora.strip():
            cursor.execute("""
                INSERT INTO agendamentos (paciente_id, medico_id, especialidade, data, hora, valor, pago, forma_pagamento, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (paciente_id, medico_id, especialidade, str(data), hora, valor, pago, forma_pagamento, status))
            conn.commit()
            st.success("Consulta agendada com sucesso!")
        else:
            st.error("Preencha todos os campos corretamente.")
    conn.close()

def ver_agenda():
    st.title("📋 Agenda do Dia - Com Filtros")

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    data_selecionada = st.date_input("Selecione a data", value=date.today())

    cursor.execute("SELECT nome FROM medicos")
    medicos = [m[0] for m in cursor.fetchall()]
    medicos.insert(0, "Todos")

    cursor.execute("SELECT DISTINCT especialidade FROM medicos")
    especialidades = [e[0] for e in cursor.fetchall()]
    especialidades.insert(0, "Todos")

    status_opcoes = ["Todos", "Agendado", "Confirmado", "Reagendado", "Cancelado"]
    pago_opcoes = ["Todos", "Sim", "Não"]

    filtro_medico = st.selectbox("Filtrar por Médico", medicos)
    filtro_especialidade = st.selectbox("Filtrar por Especialidade", especialidades)
    filtro_status = st.selectbox("Filtrar por Status", status_opcoes)
    filtro_pago = st.selectbox("Filtrar por Pagamento", pago_opcoes)

    query = """
        SELECT 
            a.id,
            p.nome,
            p.telefone,
            m.nome,
            a.especialidade,
            a.data,
            a.hora,
            a.valor,
            a.pago,
            a.forma_pagamento,
            a.status,
            a.presenca
        FROM agendamentos a
        JOIN pacientes p ON a.paciente_id = p.id
        JOIN medicos m ON a.medico_id = m.id
        WHERE a.data = ?
    """
    params = [str(data_selecionada)]

    if filtro_medico != "Todos":
        query += " AND m.nome = ?"
        params.append(filtro_medico)
    if filtro_especialidade != "Todos":
        query += " AND a.especialidade = ?"
        params.append(filtro_especialidade)
    if filtro_status != "Todos":
        query += " AND a.status = ?"
        params.append(filtro_status)
    if filtro_pago != "Todos":
        query += " AND a.pago = ?"
        params.append(filtro_pago)

    query += " ORDER BY a.hora"

    cursor.execute(query, params)
    agendamentos = cursor.fetchall()

    if not agendamentos:
        st.info("Nenhum agendamento encontrado para os filtros selecionados.")
        conn.close()
        return

    for ag in agendamentos:
        st.markdown(f"""
        **Paciente:** {ag[1]}  
        **Telefone:** {ag[2]}  
        **Médico:** {ag[3]}  
        **Especialidade:** {ag[4]}  
        **Data:** {ag[5]}  
        **Hora:** {ag[6]}  
        **Valor:** R$ {ag[7]:.2f}  
        **Pago:** {ag[8]}  
        **Forma de pagamento:** {ag[9]}  
        **Status:** {ag[10]}  
        **Presença:** {ag[11]}  
        ---
        """)

    conn.close()

def ver_agenda_medico(nome_medico):
    st.title(f"📅 Minha Agenda - Dr(a). {nome_medico}")

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    data_selecionada = st.date_input("Selecione a data", value=date.today())

    query = """
        SELECT 
            a.id,
            p.nome,
            p.telefone,
            a.especialidade,
            a.data,
            a.hora,
            a.valor,
            a.pago,
            a.forma_pagamento,
            a.status,
            a.presenca
        FROM agendamentos a
        JOIN pacientes p ON a.paciente_id = p.id
        JOIN medicos m ON a.medico_id = m.id
        WHERE m.nome = ? AND a.data = ?
        ORDER BY a.hora
    """

    cursor.execute(query, (nome_medico, str(data_selecionada)))
    agendamentos = cursor.fetchall()

    if not agendamentos:
        st.info("Nenhum agendamento encontrado para esta data.")
        conn.close()
        return

    for ag in agendamentos:
        st.markdown(f"""
        **Paciente:** {ag[1]}  
        **Telefone:** {ag[2]}  
        **Especialidade:** {ag[3]}  
        **Data:** {ag[4]}  
        **Hora:** {ag[5]}  
        **Valor:** R$ {ag[6]:.2f}  
        **Pago:** {ag[7]}  
        **Forma de pagamento:** {ag[8]}  
        **Status:** {ag[9]}  
        **Presença:** {ag[10]}  
        ---
        """)

    conn.close()
