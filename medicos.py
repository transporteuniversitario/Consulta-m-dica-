import streamlit as st
import sqlite3

def cadastrar_medicos():
    st.title("👨‍⚕️ Cadastro de Médicos")

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, especialidade, dias_atendimento FROM medicos ORDER BY nome")
    medicos = cursor.fetchall()

    st.subheader("Médicos cadastrados")
    for m in medicos:
        st.write(f"ID: {m[0]} | Nome: {m[1]} | Especialidade: {m[2]} | Dias de Atendimento: {m[3]}")
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button(f"Editar {m[1]}", key=f"editar_med_{m[0]}"):
                st.session_state["edit_med_id"] = m[0]
                st.experimental_rerun()
        with col2:
            if st.button(f"Excluir {m[1]}", key=f"excluir_med_{m[0]}"):
                confirmar = st.checkbox(f"Confirma exclusão de {m[1]}?", key=f"confirma_med_{m[0]}")
                if confirmar:
                    cursor.execute("DELETE FROM medicos WHERE id = ?", (m[0],))
                    conn.commit()
                    st.success(f"Médico {m[1]} excluído.")
                    st.experimental_rerun()

    st.markdown("---")

    if "edit_med_id" in st.session_state:
        editar_medico(st.session_state["edit_med_id"])
        return

    st.subheader("Cadastrar novo médico")
    nome = st.text_input("Nome do médico")
    especialidade = st.text_input("Especialidade")
    dias_atendimento = st.text_input("Dias de atendimento (ex: Seg, Qua, Sex)")

    if st.button("Cadastrar médico"):
        if nome.strip() and especialidade.strip():
            cursor.execute("INSERT INTO medicos (nome, especialidade, dias_atendimento) VALUES (?, ?, ?)",
                           (nome, especialidade, dias_atendimento))
            conn.commit()
            st.success(f"Médico {nome} cadastrado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Preencha pelo menos o nome e especialidade.")

    conn.close()

def editar_medico(med_id):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT nome, especialidade, dias_atendimento FROM medicos WHERE id = ?", (med_id,))
    medico = cursor.fetchone()
    if not medico:
        st.error("Médico não encontrado.")
        return

    st.subheader(f"Editar médico: {medico[0]}")

    novo_nome = st.text_input("Nome", value=medico[0])
    nova_esp = st.text_input("Especialidade", value=medico[1])
    novos_dias = st.text_input("Dias de atendimento", value=medico[2])

    if st.button("Salvar alterações"):
        if novo_nome.strip() and nova_esp.strip():
            cursor.execute("UPDATE medicos SET nome = ?, especialidade = ?, dias_atendimento = ? WHERE id = ?",
                           (novo_nome, nova_esp, novos_dias, med_id))
            conn.commit()
            st.success("Médico atualizado!")
            del st.session_state["edit_med_id"]
            st.experimental_rerun()
        else:
            st.error("Nome e especialidade são obrigatórios.")

    conn.close()
