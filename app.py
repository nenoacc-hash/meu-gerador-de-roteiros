import streamlit as st
import google.generativeai as genai
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Geny: Roteiros Inteligentes", page_icon="🎬")

# Link da sua planilha
SHEET_ID = "1uB2n6wPK8K5aC_6RUKB27M_vn2u7o9thYt1JcEZMbKI"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Função de Acesso - Lê a planilha e confere a senha
def verificar_acesso(senha_digitada):
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [str(c).strip().lower() for c in df.columns]
        senha_limpa = str(senha_digitada).strip()
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
    st.title("🔑 Acesso / Access")
    idioma = st.selectbox("🌐 Idioma", ["Português", "English", "Español"])
    senha_acesso = st.text_input("Senha / Password:", type="password")

# DICIONÁRIO COMPLETO DE TRADUÇÃO
textos = {
    "Português": {
        "titulo": "🎬 Geny: Roteiros Inteligentes",
        "sub": "Crie roteiros que vendem em segundos!",
        "btn": "🚀 Gerar Roteiro",
        "neg": "Qual o seu negócio?",
        "pro": "O que quer vender?",
        "est": "Tom do Roteiro:",
        "ex_neg": "Ex: Doceria Dona Geny",
        "ex_pro": "Ex: Pavê de Sonho de Valsa",
        "tons": ["Engraçado", "Sério/Profissional", "Explicativo/Tutorial", "Urgente/Promoção", "Storytelling", "Curiosidades"],
        "aviso_erro": "Preencha todos os campos!",
        "ass_susp": "Assinatura Suspensa",
        "senha_inc": "Senha Incorreta",
        "msg_login": "👈 Insira sua senha na barra lateral."
    },
    "English": {
        "titulo": "🎬 Geny: Smart Scripts",
        "sub": "Create scripts that sell in seconds!",
        "btn": "🚀 Generate Script",
        "neg": "What is your business?",
        "pro": "What are you selling?",
        "est": "Script Tone:",
        "ex_neg": "Ex: Joe's Bakery",
        "ex_pro": "Ex: Chocolate Cake",
        "tons": ["Funny", "Professional", "Tutorial/Explainer", "Urgent/Sale", "Storytelling", "Fun Facts"],
        "aviso_erro": "Please fill in all fields!",
        "ass_susp": "Subscription Suspended",
        "senha_inc": "Incorrect Password",
        "msg_login": "👈 Enter your password on the sidebar."
    },
    "Español": {
        "titulo": "🎬 Geny: Guiones Inteligentes",
        "sub": "¡Crea guiones que venden en segundos!",
        "btn": "🚀 Generar Guion",
        "neg": "Tu negocio:",
        "pro": "¿Qué quieres vender?",
        "est": "Tono del guion:",
        "ex_neg": "Ej: Pastelería de Juana",
        "ex_pro": "Ej: Tarta de Chocolate",
        "tons": ["Divertido", "Profesional", "Explicativo", "Urgente/Oferta", "Storytelling", "Curiosidades"],
        "aviso_erro": "¡Por favor, complete todos os campos!",
        "ass_susp": "Suscripción Suspendida",
        "senha_inc": "Contraseña Incorrecta",
        "msg_login": "👈 Ingrese su contraseña en la barra lateral."
    }
}

t = textos[idioma]
st.title(t["titulo"])

# Lógica de Login
if senha_acesso:
    autorizado, mensagem = verificar_acesso(senha_acesso)
    
    if autorizado:
        st.subheader(t["sub"])
        
        if "API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["API_KEY"])
            model = genai.GenerativeModel('gemini-2.5-flash')

            col1, col2 = st.columns(2)
            with col1:
                negocio = st.text_input(t["neg"], placeholder=t["ex_neg"])
            with col2:
                produto = st.text_input(t["pro"], placeholder=t["ex_pro"])
            
            estilo = st.selectbox(t["est"], t["tons"])

            if st.button(t["btn"]):
                if negocio and produto:
                    # PROMPT BLINDADO PARA IDIOMAS
                    prompt = (
                        f"IMPORTANT: You MUST write the entire response in {idioma}. "
                        f"Atue como um roteirista de elite. Crie um roteiro de rede social para: {negocio}. "
                        f"Produto: {produto}. Tom: {estilo}. "
                        f"Traduza tudo para {idioma} e use o formato: "
                        f"1. Cena, 2. Áudio, 3. Legenda e Hashtags."
                    )
                    
                    with st.spinner("..."):
                        response = model.generate_content(prompt)
                        st.divider()
                        st.markdown(response.text)
                else:
                    st.warning(t["aviso_erro"])
        else:
            st.error("Erro: API KEY")
            
    elif mensagem == "bloqueado":
        st.error(t["ass_susp"])
    elif mensagem == "invalido":
        st.warning(t["senha_inc"])
    else:
        st.error(f"Erro: {mensagem}")
else:
    st.info(t["msg_login"])
