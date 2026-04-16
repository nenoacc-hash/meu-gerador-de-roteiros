import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Gerador de Roteiros", page_icon="🎬")

st.title("🎬 Gerador de Roteiros para Reels/TikTok")

# Barra lateral para a chave
with st.sidebar:
    st.title("Configuração")
    api_key = st.text_input("Cole sua Chave API aqui:", type="password")
    st.info("Pegue sua chave no Google AI Studio")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usando o modelo mais atual e disponível
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Campos de preenchimento
        tipo_negocio = st.text_input("Qual o seu negócio?", placeholder="Ex: Doceria Dona Geny")
        produto = st.text_input("O que quer vender?", placeholder="Ex: Pavê de Sonho de Valsa")
        estilo = st.selectbox("Estilo do vídeo:", ["Engraçado", "Profissional", "Trend Curta"])

        if st.button("Gerar Roteiro"):
            if tipo_negocio and produto:
                prompt = f"Atue como um especialista em marketing. Crie um roteiro de vídeo curto para {tipo_negocio} sobre {produto}. Estilo: {estilo}. Divida em: Cena, Fala e Legenda."
                
                with st.spinner('A IA está pensando...'):
                    response = model.generate_content(prompt)
                    st.success("Aqui está seu roteiro!")
                    st.write(response.text)
            else:
                st.warning("Por favor, preencha o negócio e o produto.")
    except Exception as e:
        st.error(f"Ops, algo deu errado: {e}")
else:
    st.warning("Por favor, insira sua chave API na barra lateral para começar.")
