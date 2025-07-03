import streamlit as st
import sqlite3

def cadastrar_pacientes():
    st.title("👥 Cadastro de Pacientes")

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, telefone, pago, forma_pagamento FROM pacientes ORDER BY nome")
    pacientes = cursor.fetchall()

    st.subheader("Pacientes cadastrados")
    for p in pacientes:
        st.write(f"ID: {p[0]} | Nome: {p[1]} | Telefone: {p[2]} | Pago: {p[3]} | Forma Pagamento: {p[4]}")
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button(f"Editar {p[1]}", key=f"editar_pac_{p[0]}"):
                st.session_state["edit_pac_id"] = p[0]
                st.experimental_rerun()
        with col2:
            if st.button(f"Excluir {p[1]}", key=f"excluir_pac_{p[0]}"):
                confirmar = st.checkbox(f"Confirma exclusão de {p[1]}?", key=f"confirma_pac_{p[0]}")
                if confirmar:
                    cursor.execute("DELETE FROM pacientes WHERE id = ?", (p[0],))
                    conn.commit()
                    st.success(f"Paciente {p[1]} excluído.")
                    st.experimental_rerun()

    st.markdown("---")

    if "edit_pac_id" in st.session_state:
        editar_paciente(st.session_state["edit_pac_id"])
        return

    st.subheader("Cadastrar novo paciente")
    nome = st.text_input("Nome do paciente")
    telefone = st.text_input("Telefone")
    pago = st.selectbox("Pagamento realizado?", ["Não", "Sim"])
    forma_pagamento = st.text_input("Forma de pagamento")

    if st.button("Cadastrar paciente"):
        if nome.strip():
            cursor.execute("INSERT INTO pacientes (nome, telefone, pago, forma_pagamento) VALUES (?, ?, ?, ?)",
                           (nome, telefone, pago, forma_pagamento))
            conn.commit()
            st.success(f"Paciente {nome} cadastrado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("O nome do paciente é obrigatório.")

    conn.close()

def editar_paciente(pac_id):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT nome, telefone, pago, forma_pagamento FROM pacientes WHERE id = ?", (pac_id,))
    paciente = cursor.fetchone()
    if not paciente:
        st.error("Paciente não encontrado.")
        return

    st.subheader(f"Editar paciente: {paciente[0]}")

    novo_nome = st.text_input("Nome", value=paciente[0])
    novo_telefone = st.text_input("Telefone", value=paciente[1])
    pago = st.selectbox("Pagamento realizado?", ["Não", "Sim"], index=0 if paciente[2]=="Não" else 1)
    forma_pagamento = st.text_input("Forma de pagamento", value=paciente[3])

    if st.button("Salvar alterações"):
        if novo_nome.strip():
            cursor.execute("UPDATE pacientes SET nome = ?, telefone = ?, pago = ?, forma_pagamento = ? WHERE id = ?",
                           (novo_nome, novo_telefone, pago, forma_pagamento, pac_id))
            conn.commit()
            st.success("Paciente atualizado!")
            del st.session_state["edit_pac_id"]
            st.experimental_rerun()
        else:
            st.error("O nome do paciente é obrigatório.")

    conn.close()
