import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gerador de Roteiros", page_icon="🎬")
st.title("🎬 Gerador de Roteiros para Reels")

with st.sidebar:
    api_key = st.text_input("Cole sua Chave API aqui:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # TENTATIVA 1: Modelo Pro (O mais comum de funcionar)
        model = genai.GenerativeModel('gemini-pro')

        tipo_negocio = st.text_input("Seu negócio:", placeholder="Ex: Doceria Dona Geny")
        produto = st.text_input("O que quer vender?", placeholder="Ex: Pavê de Sonho de Valsa")

        if st.button("Gerar Roteiro"):
            if tipo_negocio and produto:
                prompt = f"Crie um roteiro de Reels de 15 segundos para {tipo_negocio} sobre {produto}. Divida em: Cena, Fala e Legenda."
                with st.spinner('Gerando...'):
                    # Se o gemini-pro falhar, ele vai tentar o flash automaticamente
                    try:
                        response = model.generate_content(prompt)
                    except:
                        model_flash = genai.GenerativeModel('gemini-1.5-flash')
                        response = model_flash.generate_content(prompt)
                        
                    st.success("Sucesso!")
                    st.write(response.text)
            else:
                st.warning("Preencha os campos!")
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
else:
    st.info("Insira a chave API na esquerda.")
