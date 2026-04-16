import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Gerador de Roteiros Lucrativos", page_icon="🎬")

st.title("🎬 Gerador de Roteiros para Reels/TikTok")
st.subheader("Crie roteiros que vendem em segundos!")

# Aqui você colocaria sua chave da API do Google (que é gratuita)
# Para testar, vamos simular a lógica
api_key = st.sidebar.text_input("Cole sua Chave API aqui", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Campos que o seu cliente vai preencher
    tipo_negocio = st.text_input("Qual o seu negócio? (Ex: Padaria, Loja de Roupas, Mecânica)")
    produto = st.text_input("O que você quer vender hoje? (Ex: Bolo de cenoura, Promoção de Pneus)")
    estilo = st.selectbox("Estilo do vídeo:", ["Engraçado", "Sério/Profissional", "Rápido/Trend", "Explicativo"])

    if st.button("Gerar Roteiro"):
        prompt = f"Crie um roteiro de 15 a 30 segundos para um Reels de um(a) {tipo_negocio} sobre {produto}. O estilo deve ser {estilo}. Divida em: O que mostrar na câmera, O que falar e Sugestão de legenda com hashtags."
        
        with st.spinner('Criando seu roteiro de milhões...'):
            response = model.generate_content(prompt)
            st.success("Prontinho! Aqui está seu roteiro:")
            st.markdown(response.text)
else:
    st.info("Para começar, você precisa de uma Chave API gratuita do Google. É só buscar por 'Google AI Studio' e gerar a sua.")

st.divider()
st.caption("Desenvolvido para ajudar o comércio local a brilhar nas redes sociais.")
