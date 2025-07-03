import streamlit as st
import sqlite3

def gerenciar_usuarios():
    st.title("👥 Gerenciamento de Usuários")

    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, usuario, tipo FROM usuarios ORDER BY usuario")
    usuarios = cursor.fetchall()

    st.subheader("Usuários cadastrados")
    for u in usuarios:
        st.write(f"ID: {u[0]} | Usuário: {u[1]} | Tipo: {u[2]}")
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button(f"Editar {u[1]}", key=f"editar_{u[0]}"):
                st.session_state["edit_user_id"] = u[0]
                st.experimental_rerun()
        with col2:
            if st.button(f"Excluir {u[1]}", key=f"excluir_{u[0]}"):
                confirmar = st.checkbox(f"Confirma exclusão de {u[1]}?", key=f"confirma_{u[0]}")
                if confirmar:
                    cursor.execute("DELETE FROM usuarios WHERE id = ?", (u[0],))
                    conn.commit()
                    st.success(f"Usuário {u[1]} excluído.")
                    st.experimental_rerun()

    st.markdown("---")

    if "edit_user_id" in st.session_state:
        editar_usuario(st.session_state["edit_user_id"])
        return

    st.subheader("Cadastrar novo usuário")
    novo_usuario = st.text_input("Nome do usuário")
    nova_senha = st.text_input("Senha", type="password")
    tipo_usuario = st.selectbox("Tipo de usuário", ["admin", "secretaria", "medico"])
    if st.button("Cadastrar usuário"):
        if novo_usuario and nova_senha:
            try:
                cursor.execute("INSERT INTO usuarios (usuario, senha, tipo) VALUES (?, ?, ?)", (novo_usuario, nova_senha, tipo_usuario))
                conn.commit()
                st.success(f"Usuário {novo_usuario} cadastrado com sucesso!")
                st.experimental_rerun()
            except sqlite3.IntegrityError:
                st.error("Usuário já existe.")
        else:
            st.error("Preencha todos os campos.")

    conn.close()

def editar_usuario(user_id):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("SELECT usuario, tipo FROM usuarios WHERE id = ?", (user_id,))
    usuario = cursor.fetchone()
    if not usuario:
        st.error("Usuário não encontrado.")
        return

    st.subheader(f"Editar usuário: {usuario[0]}")

    novo_tipo = st.selectbox("Tipo", ["admin", "secretaria", "medico"], index=["admin", "secretaria", "medico"].index(usuario[1]))
    nova_senha = st.text_input("Nova senha (deixe em branco para manter)")

    if st.button("Salvar alterações"):
        if nova_senha.strip():
            cursor.execute("UPDATE usuarios SET tipo = ?, senha = ? WHERE id = ?", (novo_tipo, nova_senha, user_id))
        else:
            cursor.execute("UPDATE usuarios SET tipo = ? WHERE id = ?", (novo_tipo, user_id))
        conn.commit()
        st.success("Usuário atualizado!")
        del st.session_state["edit_user_id"]
        st.experimental_rerun()

    conn.close()
