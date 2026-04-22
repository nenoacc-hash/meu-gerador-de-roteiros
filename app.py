import streamlit as st
import google.generativeai as genai

st.title("Diagnóstico GENY.AI")

if "API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["API_KEY"])
        st.write("### Modelos disponíveis para sua chave:")
        
        # Isso vai listar todos os modelos que sua chave tem permissão para usar
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        for m in modelos:
            st.success(f"Disponível: {m}")
            
    except Exception as e:
        st.error(f"Erro na Chave API: {e}")
else:
    st.warning("API_KEY não encontrada nos Secrets.")
