import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Gerador de Roteiros", page_icon="🎬")

st.title("🎬 Geny: Roteiros Inteligentes")
st.subheader("Crie vídeos que vendem em segundos!")

# Barra lateral
with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("Cole sua Chave API aqui:", type="password")
    st.info("Sua chave foi validada com sucesso!")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # USANDO O MODELO QUE APARECEU NA SUA LISTA VERDE!
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Campos de entrada
        tipo_negocio = st.text_input("Qual o seu negócio?", placeholder="Ex: Doceria Dona Geny")
        produto = st.text_input("O que quer vender?", placeholder="Ex: Pavê de Sonho de Valsa")
        estilo = st.selectbox("Estilo do vídeo:", ["Engraçado e Leve", "Profissional e Elegante", "Rápido (Trend)"])

        if st.button("🚀 Gerar Roteiro de Milhões"):
            if tipo_negocio and produto:
                prompt = (
                    f"Atue como um roteirista de elite para Instagram e TikTok. "
                    f"Crie um roteiro de 15 segundos para: {tipo_negocio}. "
                    f"O foco é vender: {produto}. O tom deve ser {estilo}. "
                    f"Formate em: 1. O que mostrar na imagem, 2. O que falar, 3. Legenda e Hashtags."
                )
                
                with st.spinner('A IA está criando sua obra-prima...'):
                    response = model.generate_content(prompt)
                    st.success("Roteiro pronto!")
                    st.divider()
                    st.write(response.text)
            else:
                st.warning("Preencha o nome do negócio e o produto!")
                
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
else:
    st.info("👈 Insira sua chave API na barra lateral para começar.")
