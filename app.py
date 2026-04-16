import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Geny: Roteiros Inteligentes", page_icon="🎬")

# Título e Idioma
idioma = st.sidebar.selectbox("🌐 Idioma / Language", ["Português", "English", "Español"])

titulos = {
    "Português": "🎬 Geny: Roteiros Inteligentes",
    "English": "🎬 Geny: Smart Scripts",
    "Español": "🎬 Geny: Guiones Inteligentes"
}

st.title(titulos[idioma])

# PUXANDO A CHAVE DAS CONFIGURAÇÕES SECRETAS
# Você vai configurar isso no painel do Streamlit (explico abaixo)
if "API_KEY" in st.secrets:
    api_key = st.secrets["API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # Textos por idioma
    labels = {
        "Português": ["Qual o seu negócio?", "O que quer vender?", "Estilo:", "Gerar Roteiro"],
        "English": ["Your business?", "What to sell?", "Style:", "Generate Script"],
        "Español": ["¿Tu negocio?", "¿Qué vender?", "Estilo:", "Generar Guion"]
    }

    negocio = st.text_input(labels[idioma][0])
    produto = st.text_input(labels[idioma][1])
    estilo = st.selectbox(labels[idioma][2], ["Engraçado", "Profissional", "Trend"])

    if st.button(labels[idioma][3]):
        if negocio and produto:
            prompt = f"Write a 15s social media script in {idioma} for {negocio} selling {produto}. Tone: {estilo}. Format: Scene, Speech, Caption."
            with st.spinner('...'):
                response = model.generate_content(prompt)
                st.markdown(response.text)
else:
    st.error("Erro: Chave API não configurada nos Segredos do Streamlit.")
