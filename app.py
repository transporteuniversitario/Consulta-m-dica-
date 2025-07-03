import streamlit as st
from utils import criar_tabelas
from usuarios import gerenciar_usuarios
from agenda import ver_agenda, agendar_consulta, ver_agenda_medico
from dashboard import dashboard
from relatorios import relatorios_mensais
from medicos import cadastrar_medicos
from pacientes import cadastrar_pacientes

def login():
    st.title("🔐 Login")

    if "logado" not in st.session_state:
        st.session_state["logado"] = False
    if "tipo" not in st.session_state:
        st.session_state["tipo"] = None
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    if st.session_state["logado"]:
        st.success(f"Logado como {st.session_state['usuario']} ({st.session_state['tipo']})")
        if st.button("Sair"):
            st.session_state["logado"] = False
            st.session_state["usuario"] = None
            st.session_state["tipo"] = None
            st.experimental_rerun()
        return True

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")


    
    if st.button("Entrar"):
        import sqlite3
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("SELECT tipo FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            st.session_state["logado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["tipo"] = resultado[0]
            st.success(f"Bem-vindo, {usuario}!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")
    return False

def main():
    criar_tabelas()


    # ⚠️ Trecho TEMPORÁRIO: botão para criar usuário admin
if st.sidebar.button("⚙️ Criar usuário admin"):
    import sqlite3
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuarios (usuario, senha, tipo)
            VALUES (?, ?, ?)
        """, ("admin", "admin123", "admin"))
        conn.commit()
        st.sidebar.success("Usuário admin criado com sucesso!")
    except sqlite3.IntegrityError:
        st.sidebar.warning("Usuário admin já existe.")
    conn.close()


    if not login():
        return

    tipo = st.session_state["tipo"]

    if tipo == "admin":
        menu_opcoes = [
            "Início",
            "Cadastro de Médicos",
            "Cadastro de Pacientes",
            "Agendamento",
            "Agenda do Dia",
            "Dashboard",
            "Relatórios Mensais",
            "Gerenciar Usuários",
            "Sair"
        ]
    elif tipo == "secretaria":
        menu_opcoes = [
            "Início",
            "Cadastro de Médicos",
            "Cadastro de Pacientes",
            "Agendamento",
            "Agenda do Dia",
            "Sair"
        ]
    elif tipo == "medico":
        menu_opcoes = [
            "Início",
            "Minha Agenda",
            "Sair"
        ]
    else:
        st.error("Tipo de usuário desconhecido.")
        return

    opcao = st.sidebar.selectbox("Escolha uma opção", menu_opcoes)

    if opcao == "Sair":
        st.session_state["logado"] = False
        st.session_state["usuario"] = None
        st.session_state["tipo"] = None
        st.experimental_rerun()

    elif opcao == "Cadastro de Médicos":
        cadastrar_medicos()
    elif opcao == "Cadastro de Pacientes":
        cadastrar_pacientes()
    elif opcao == "Agendamento":
        agendar_consulta()
    elif opcao == "Agenda do Dia":
        ver_agenda()
    elif opcao == "Minha Agenda":
        ver_agenda_medico(st.session_state["usuario"])
    elif opcao == "Dashboard":
        dashboard()
    elif opcao == "Relatórios Mensais":
        relatorios_mensais()
    elif opcao == "Gerenciar Usuários":
        gerenciar_usuarios()
    else:
        st.write("Bem-vindo ao sistema!")

if __name__ == "__main__":
    main()
