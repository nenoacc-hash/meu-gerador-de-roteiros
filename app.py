import streamlit as st
import google.generativeai as genai
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Geny: Roteiros Inteligentes", page_icon="🎬")

# Link da sua planilha formatado para exportação CSV
SHEET_ID = "1uB2n6wPK8K5aC_6RUKB27M_vn2u7o9thYt1JcEZMbKI"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Função para verificar acesso
def verificar_acesso(senha_digitada):
    try:
        df = pd.read_csv(SHEET_URL)
        # Limpar espaços em branco dos dados
        df['senha'] = df['senha'].astype(str).str.strip()
        df['status'] = df['status'].astype(str).str.strip().lower()
        
        # Procura a senha na planilha
        usuario = df[df['senha'] == senha_digitada]
        
        if not usuario.empty:
            if usuario.iloc[0]['status'] == 'ativo':
                return True, "sucesso"
            else:
                return False, "bloqueado"
        return False, "invalido"
    except Exception as e:
        return False, f"erro: {e}"

# Barra lateral para Idioma e Login
with st.sidebar:
    st.title("🔑 Acesso")
    idioma = st.selectbox("🌐 Idioma", ["Português", "English", "Español"])
    senha_acesso = st.text_input("Senha de Acesso:", type="password")

# Dicionário de traduções
textos = {
    "Português": {"titulo": "🎬 Geny: Roteiros Inteligentes", "sub": "Crie roteiros que vendem!", "btn": "🚀 Gerar Roteiro"},
    "English": {"titulo": "🎬 Geny: Smart Scripts", "sub": "Create scripts that sell!", "btn": "🚀 Generate Script"},
    "Español": {"titulo": "🎬 Geny: Guiones Inteligentes", "sub": "¡Guiones que venden!", "btn": "🚀 Generar Guion"}
}
t = textos[idioma]

st.title(t["titulo"])

# LÓGICA DE ACESSO
if senha_acesso:
    autorizado, mensagem = verificar_acesso(senha_acesso)
    
    if autorizado:
        st.subheader(t["sub"])
        
        if "API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["API_KEY"])
            model = genai.GenerativeModel('gemini-2.5-flash')

            negocio = st.text_input("Negócio / Business:")
            produto = st.text_input("Produto / Product:")
            
            if st.button(t["btn"]):
                if negocio and produto:
                    prompt = f"Write a 15s social media script in {idioma} for {negocio} about {produto}. Format: Scene, Speech, Caption."
                    with st.spinner("..."):
                        response = model.generate_content(prompt)
                        st.divider()
                        st.markdown(response.text)
        else:
            st.error("Erro técnico: Chave API não configurada.")
            
    elif mensagem == "bloqueado":
        st.error("Sua assinatura está suspensa. Entre em contato com o suporte.")
    elif mensagem == "invalido":
        st.warning("Senha incorreta. Verifique os dados.")
    else:
        st.error(f"Erro ao conectar com banco de dados: {mensagem}")
else:
    st.info("👈 Por favor, insira sua senha de acesso na barra lateral.")
