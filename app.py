import streamlit as st
import google.generativeai as genai
import pandas as pd
import random

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="GENY.AI: Roteiros Inteligentes", page_icon="🎬")

# ID exato da sua planilha
SHEET_ID = "1-_7_95rP5k0n19NWY5cw-CpFYK8hHuw3I7e11_eUdGY"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&v={random.randint(1, 99999)}"

def verificar_acesso(senha_digitada):
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [str(c).strip().lower() for c in df.columns]
        senha_limpa = str(senha_digitada).strip()
        
        for index, row in df.iterrows():
            if str(row['senha']).strip() == senha_limpa:
                status_venda = str(row['status']).strip().lower()
                if status_venda in ['pago', 'ativo']:
                    return True, "sucesso"
                else:
                    return False, "bloqueado"
        return False, "invalido"
    except Exception as e:
        return False, f"erro: {e}"

# 2. BARRA LATERAL
with st.sidebar:
    st.title("🔑 Acesso / Access")
    idioma = st.selectbox("🌐 Idioma", ["Português", "English", "Español"])
    senha_acesso = st.text_input("Senha / Password:", type="password")
    if st.button("🔄 Atualizar / Refresh"):
        st.rerun()

# 3. DICIONÁRIO DE TEXTOS
textos = {
    "Português": {
        "titulo": "🎬 GENY.AI: Roteiros Inteligentes",
        "sub": "Crie roteiros que vendem em segundos!",
        "btn": "🚀 Gerar Roteiro",
        "neg": "Qual o seu negócio?",
        "pro": "O que quer vender?",
        "est": "Tom do Roteiro:",
        "plat": "Onde vai postar?",
        "ex_neg": "Ex: Doceria Dona Geny",
        "ex_pro": "Ex: Pavê de Sonho de Valsa",
        "tons": ["Engraçado", "Sério/Profissional", "Explicativo/Tutorial", "Urgente/Promoção", "Storytelling", "Curiosidades"],
        "redes": ["Instagram (Reels)", "TikTok", "YouTube Shorts", "WhatsApp (Status)", "Facebook"],
        "aviso_erro": "Preencha todos os campos!",
        "msg_login": "👈 Insira sua senha na barra lateral."
    },
    "English": { "titulo": "🎬 GENY.AI: Smart Scripts", "sub": "Create scripts that sell in seconds!", "btn": "🚀 Generate Script", "neg": "What is your business?", "pro": "What are you selling?", "est": "Script Tone:", "plat": "Where will you post?", "ex_neg": "Ex: Joe's Bakery", "ex_pro": "Ex: Chocolate Cake", "tons": ["Funny", "Professional", "Tutorial/Explainer", "Urgent/Sale", "Storytelling", "Fun Facts"], "redes": ["Instagram (Reels)", "TikTok", "YouTube Shorts", "WhatsApp Status", "Facebook"], "aviso_erro": "Please fill in all fields!", "msg_login": "👈 Enter your password on the sidebar." },
    "Español": { "titulo": "🎬 GENY.AI: Guiones Inteligentes", "sub": "Crea guiones que venden en segundos!", "btn": "🚀 Generar Guion", "neg": "Tu negocio:", "pro": "Qué quieres vender?", "est": "Tono del guion:", "plat": "Dónde vas a publicar?", "ex_neg": "Ej: Pastelería de Juana", "ex_pro": "Ej: Tarta de Chocolate", "tons": ["Divertido", "Profesional", "Explicativo", "Urgente/Oferta", "Storytelling", "Curiosidades"], "redes": ["Instagram (Reels)", "TikTok", "YouTube Shorts", "WhatsApp Status", "Facebook"], "aviso_erro": "¡Por favor, complete todos los campos!", "msg_login": "👈 Ingrese su contraseña en la barra lateral." }
}

t = textos[idioma]
st.title(t["titulo"])

# 4. LÓGICA PRINCIPAL
if senha_acesso:
    autorizado, mensagem = verificar_acesso(senha_acesso)
    
    if autorizado:
        st.subheader(t["sub"])
        
        # AJUSTE DA API_KEY (FORÇADO E ROBUSTO)
        api_key = st.secrets.get("API_KEY")
        
        if api_key:
            genai.configure(api_key=api_key)
            # USANDO O MODELO PADRÃO MAIS ESTÁVEL PARA 2026
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
            
            col1, col2 = st.columns(2)
            with col1: negocio = st.text_input(t["neg"], placeholder=t["ex_neg"])
            with col2: produto = st.text_input(t["pro"], placeholder=t["ex_pro"])
            
            col3, col4 = st.columns(2)
            with col3: estilo = st.selectbox(t["est"], t["tons"])
            with col4: plataforma = st.selectbox(t["plat"], t["redes"])

            if st.button(t["btn"]):
                if negocio and produto:
                    prompt = (f"Write in {idioma}. Atue como um roteirista de elite para {plataforma}. "
                              f"Crie um roteiro de 15 a 30 segundos para o negócio {negocio}. "
                              f"Produto: {produto}. Tom: {estilo}. "
                              f"Formato: 1. Cena, 2. Áudio, 3. Legenda e Hashtags.")
                    try:
                        with st.spinner("Gerando roteiro de elite..."):
                            response = model.generate_content(prompt)
                            st.divider()
                            st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Erro ao gerar conteúdo: {e}")
                else:
                    st.warning(t["aviso_erro"])
        else:
            st.error("Configuração de API pendente nos Secrets.")
    elif mensagem == "bloqueado":
        st.error("Acesso Suspenso (Verifique sua assinatura)")
    elif mensagem == "invalido":
        st.warning("Senha Incorreta")
else:
    st.info(t["msg_login"])
