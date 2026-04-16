import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Geny: Roteiros Inteligentes", page_icon="🎬")

# Barra lateral para Idioma
idioma = st.sidebar.selectbox("🌐 Idioma / Language", ["Português", "English", "Español"])

# Dicionário de traduções para a interface
textos = {
    "Português": {
        "titulo": "🎬 Geny: Roteiros Inteligentes",
        "subtitulo": "Crie roteiros que vendem em segundos!",
        "label_negocio": "Qual o seu negócio?",
        "label_produto": "O que quer vender?",
        "label_estilo": "Estilo do vídeo:",
        "botao": "🚀 Gerar Roteiro",
        "placeholder_negocio": "Ex: Doceria Dona Geny",
        "spinner": "A IA está criando sua obra-prima..."
    },
    "English": {
        "titulo": "🎬 Geny: Smart Scripts",
        "subtitulo": "Create scripts that sell in seconds!",
        "label_negocio": "What is your business?",
        "label_produto": "What do you want to sell?",
        "label_estilo": "Video style:",
        "botao": "🚀 Generate Script",
        "placeholder_negocio": "Ex: Bakery, Coffee Shop",
        "spinner": "The AI is creating your masterpiece..."
    },
    "Español": {
        "titulo": "🎬 Geny: Guiones Inteligentes",
        "subtitulo": "¡Crea guiones que venden em segundos!",
        "label_negocio": "Tu negocio:",
        "label_produto": "Qué quieres vender?",
        "label_estilo": "Estilo del video:",
        "botao": "🚀 Generar Guion",
        "placeholder_negocio": "Ej: Pastelería, Cafetería",
        "spinner": "A IA está criando tu obra maestra..."
    }
}

t = textos[idioma]

st.title(t["titulo"])
st.subheader(t["subtitulo"]) # O GANCHO VOLTOU AQUI!

if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')

    negocio = st.text_input(t["label_negocio"], placeholder=t["placeholder_negocio"])
    produto = st.text_input(t["label_produto"])
    estilo = st.selectbox(t["label_estilo"], ["Engraçado", "Profissional", "Trend"])

    if st.button(t["botao"]):
        if negocio and produto:
            prompt = f"Write a 15s social media script in {idioma} for {negocio} about {produto}. Tone: {estilo}. Format: Scene, Speech, Caption."
            with st.spinner(t["spinner"]):
                response = model.generate_content(prompt)
                st.divider()
                st.markdown(response.text)
        else:
            st.warning("Preencha todos os campos!")
else:
    st.error("Erro: Chave API não configurada nos Segredos do Streamlit.")
