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
        # Lê a planilha
        df = pd.read_csv(SHEET_URL)
        
        # Ajusta os nomes das colunas para tirar espaços e ficar tudo minúsculo
        df.columns = df.columns.str.strip().str.lower()
        
        # Limpa os dados das colunas de senha e status
        df['senha'] = df['senha'].astype(str).str.strip()
        df['status'] = df['status'].astype(str).str.strip().lower()
        
        # Procura a senha digitada
        usuario = df[df['senha'] == str(senha_digitada).strip()]
        
        if not usuario.empty:
            if usuario.iloc[0]['status'] == 'ativo':
                return True, "sucesso"
            else:
                return False, "bloqueado"
        return False, "invalido"
    except Exception as e:
        return False, f"erro nos dados: {e}"

# Barra lateral
with st.sidebar:
    st.title("🔑 Acesso")
    idioma = st.selectbox("🌐 Idioma", ["Português", "English", "Español"])
    senha_acesso = st.text_input("Senha de Acesso:", type="password")

# Dicionário de traduções
textos = {
    "Português": {"titulo": "🎬 Geny: Roteiros Inteligentes", "sub": "Crie roteiros que vendem!", "btn": "🚀 Gerar Roteiro", "neg": "Qual o seu negócio?", "pro": "O que quer vender?"},
    "English": {"titulo": "🎬 Geny: Smart Scripts", "sub": "Create scripts that sell!", "btn": "🚀 Generate Script", "neg": "Your business?", "pro": "What to sell?"},
    "Español": {"titulo": "🎬 Geny: Guiones Inteligentes", "sub": "¡Guiones que venden!", "btn": "🚀 Generar Guion", "neg": "Tu negocio:", "pro": "¿Qué vender?"}
}
t = textos[idioma]

st.title(t["titulo"])

if senha_acesso:
    autorizado, mensagem = verificar_acesso(senha_acesso)
    
    if autorizado:
        st.subheader(t["sub"])
        
        if "API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["API_KEY"])
            model = genai.GenerativeModel('gemini-2.5-flash')

            negocio = st.text_input(t["neg"])
            produto = st.text_input(t["pro"])
            
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
