import streamlit as st
import urllib.parse

def enviar_whatsapp(telefone, mensagem):
    # Remove símbolos e espaços do telefone
    numero = ''.join(filter(str.isdigit, telefone))

    # Constrói a URL do WhatsApp Web
    mensagem_codificada = urllib.parse.quote(mensagem)
    url = f"https://wa.me/{numero}?text={mensagem_codificada}"

    # Botão para abrir link do WhatsApp
    st.markdown(f"""
    <a href="{url}" target="_blank">
        <button style='background-color: #25D366; color: white; border: none; padding: 6px 10px; border-radius: 5px; cursor: pointer;'>📲 Enviar no WhatsApp</button>
    </a>
    """, unsafe_allow_html=True)
