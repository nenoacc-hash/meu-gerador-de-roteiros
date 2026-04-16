import streamlit as st
import google.generativeai as genai

st.title("🧪 Teste de Conexão com o Google")

api_key = st.sidebar.text_input("Chave API:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        st.write("Tentando listar modelos disponíveis...")
        # Este comando pergunta ao Google: 'O que eu posso usar?'
        modelos = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modelos.append(m.name)
        
        if modelos:
            st.success(f"Conectado! Você pode usar estes modelos: {modelos}")
            st.info("Agora escolha um deles para testar:")
            escolha = st.selectbox("Selecione o modelo:", modelos)
            
            if st.button("Testar Oi da IA"):
                model = genai.GenerativeModel(escolha)
                response = model.generate_content("Dê um oi para a Dona Geny!")
                st.write(response.text)
        else:
            st.warning("A chave funcionou, mas o Google não liberou nenhum modelo de IA para você.")
            
    except Exception as e:
        st.error(f"Erro Real: {e}")
else:
    st.info("Insira a chave na esquerda.")
