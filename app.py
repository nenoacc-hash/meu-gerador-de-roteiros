import streamlit as st
import google.generativeai as genai

# Título do App
st.set_page_config(page_title="Gerador de Roteiros", page_icon="🎬")
st.title("🎬 Gerador de Roteiros para Reels")

# Barra lateral para a chave
with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("Cole sua Chave API aqui:", type="password")

if api_key:
    try:
        # Configuração simplificada
        genai.configure(api_key=api_key)
        
        # O segredo: Não vamos especificar v1 ou v1beta, vamos deixar a biblioteca decidir
        model = genai.GenerativeModel('gemini-1.5-flash')

        tipo_negocio = st.text_input("Seu negócio:", placeholder="Ex: Doceria Dona Geny")
        produto = st.text_input("O que quer vender?", placeholder="Ex: Pavê de Sonho de Valsa")

        if st.button("Gerar Roteiro"):
            if tipo_negocio and produto:
                prompt = f"Crie um roteiro de Reels de 15 segundos para {tipo_negocio} sobre {produto}. Divida em: Cena, Fala e Legenda."
                with st.spinner('A IA está trabalhando...'):
                    # Comando de geração pura
                    response = model.generate_content(prompt)
                    st.success("Roteiro Criado!")
                    st.write(response.text)
            else:
                st.warning("Por favor, preencha os campos de texto.")
                
    except Exception as e:
        # Se der erro, ele vai nos dizer exatamente o que é sem travar
        st.error(f"Atenção: Verifique sua chave API ou a conexão. Detalhe: {e}")
else:
    st.info("👈 Insira sua chave API ali na barra lateral para começar.")
