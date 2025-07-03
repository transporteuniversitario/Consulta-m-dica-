import streamlit as st
st.write("Versão do Streamlit:", st.__version__)
from utils import criar_tabelas
from usuarios import gerenciar_usuarios
from agenda import ver_agenda, agendar_consulta, ver_agenda_medico
from dashboard import dashboard
from relatorios import relatorios_mensais
from medicos import cadastrar_medicos
from pacientes import cadastrar_pacientes


import streamlit as st


    


import os

logo_path = "static/logo_sao_lucas.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=100)
else:
    st.warning("⚠️ Logo não encontrado. Verifique o caminho: static/logo_sao_lucas.png")
    

st.set_page_config(
    page_title="São Lucas - Agendamentos",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="auto"
)



def login():
    st.set_page_config(page_title="São Lucas - Login", layout="centered")

    # HTML + CSS customizado
    st.markdown("""
        <style>
            body {
                background-color: #f0f2f6;
            }
            .login-box {
                max-width: 420px;
                margin: 5vh auto;
                padding: 40px;
                background-color: white;
                border-radius: 12px;
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            .login-box img {
                width: 160px;
                margin-bottom: 25px;
            }
            .login-title {
                font-size: 26px;
                font-weight: bold;
                color: #056644;
                margin-bottom: 25px;
            }
            .stButton>button {
                background-color: #056644;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                width: 100%;
            }
            .stTextInput>div>div>input {
                padding: 10px;
                border-radius: 6px;
                border: 1px solid #ccc;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.image("static/logo_sao_lucas.png")  # ✅ Só um logo aqui
    st.markdown('<div class="login-title">🔐 Login</div>', unsafe_allow_html=True)

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
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")

    st.markdown('</div>', unsafe_allow_html=True)

    return st.session_state.get("logado", False)



def main():
    criar_tabelas()

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
        st.rerun()  # ✅ substituído

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

