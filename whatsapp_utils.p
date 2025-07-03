import streamlit as st
import urllib.parse

def enviar_whatsapp(telefone, mensagem):
    # Limpa o telefone, mantendo só dígitos
    telefone_limpo = ''.join(filter(str.isdigit, telefone))
    texto_url = urllib.parse.quote(mensagem)
    link = f"https://wa.me/{telefone_limpo}?text={texto_url}"

    # Exibe o link clicável no Streamlit
    st.markdown(f"[📱 Enviar WhatsApp]({link})", unsafe_allow_html=True)
