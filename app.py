import streamlit as st
import google.generativeai as genai
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Geny: Roteiros Inteligentes", page_icon="🎬")

# Link da sua planilha
SHEET_ID = "1uB2n6wPK8K5aC_6RUKB27M_vn2u7o9thYt1JcEZMbKI"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Função para verificar acesso - Versão Blindada
def verificar_acesso(senha_digitada):
    try:
        df = pd.read_csv(SHEET_URL)
        # Padroniza os nomes das colunas para minúsculo
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # Converte a senha digitada para texto puro e limpa espaços
        senha_limpa = str(senha_digitada).strip()
        
        # Procura a senha na coluna 'senha'
        # Usamos .values para evitar o erro de 'Series'
        for index, row in df.iterrows():
            if str(row['senha']).strip() == senha_limpa:
                if str(row['status']).strip().lower() == 'ativo':
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

# Dicionário de traduções (Gancho incluído!)
textos = {
    "Português": {"titulo": "🎬 Geny: Roteiros Inteligentes", "sub": "Crie roteiros que vendem em segundos!", "btn": "🚀 Gerar Roteiro", "neg": "Qual o seu negócio?", "pro": "O que quer vender?"},
    "English": {"titulo": "🎬 Geny: Smart Scripts", "sub": "Create scripts that sell in seconds!", "btn": "🚀 Generate Script", "neg": "Your business?", "pro": "What to sell?"},
    "Español": {"titulo": "🎬 Geny: Guiones Inteligentes", "sub": "¡Crea guiones que venden en segundos!", "btn": "🚀 Generar Guion", "neg": "Tu negocio:", "pro": "¿Qué vender?"}
}
t = textos[idioma]

st.title(t["titulo"])

# Lógica de Login
if senha_acesso:
    autorizado, mensagem = verificar_acesso(senha_acesso)
    
    if autorizado:
        st.subheader(t["sub"]) # O GANCHO VOLTOU!
        
        if "API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["API_KEY"])
            model = genai.GenerativeModel('gemini-2.5-flash')

            negocio = st.text_input(t["neg"], placeholder="Ex: Doceria Dona Geny")
            produto = st.text_input(t["pro"])
            
            if st.button(t["btn"]):
                if negocio and produto:
                    prompt = f"Write a 15s social media script in {idioma} for {negocio} about {produto}. Format: Scene, Speech, Caption."
                    with st.spinner("IA criando..."):
                        response = model.generate_content(prompt)
                        st.divider()
                        st.markdown(response.text)
        else:
            st.error("Chave API não configurada nos Secrets.")
            
    elif mensagem == "bloqueado":
        st.error("Sua assinatura está suspensa.")
    elif mensagem == "invalido":
        st.warning("Senha incorreta.")
    else:
        st.error(f"Erro: {mensagem}")
else:
    st.info("👈 Insira sua senha na barra lateral para liberar o acesso.")
