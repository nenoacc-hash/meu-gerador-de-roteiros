import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gerador de Roteiros", page_icon="🎬")
st.title("🎬 Gerador de Roteiros para Reels")

with st.sidebar:
    api_key = st.text_input("Cole sua Chave API aqui:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Este nome aqui embaixo é o 'coringa' que o Google aceita em 99% das contas de 2026
        model = genai.GenerativeModel('gemini-1.5-flash')

        tipo_negocio = st.text_input("Seu negócio:", placeholder="Ex: Doceria Dona Geny")
        produto = st.text_input("O que quer vender?", placeholder="Ex: Pavê de Sonho de Valsa")

        if st.button("Gerar Roteiro"):
            if tipo_negocio and produto:
                # Usando uma chamada mais simples para evitar o erro v1beta
                with st.spinner('A IA está trabalhando...'):
                    response = model.generate_content(
                        f"Roteiro de Reels: {tipo_negocio}, produto {produto}. Curto e chamativo."
                    )
                    st.success("Conseguimos!")
                    st.write(response.text)
            else:
                st.warning("Preencha os campos.")
                
    except Exception as e:
        st.error(f"Erro: {e}")
else:
    st.info("👈 Insira sua chave API.")
