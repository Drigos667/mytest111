import streamlit as st
import requests
import json

# Pegando a chave de forma segura via secrets
API_KEY = st.secrets["API_KEY"]

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://meusite.com",  # Pode ajustar para seu domínio
    "X-Title": "chat-openrouter-test"
}

st.set_page_config(page_title="Minha IA", page_icon="🤖")
st.title("CryptoBot")
st.write("Digite uma pergunta e veja a mágica acontecer!")

pergunta = st.text_input("Sua pergunta:")

if st.button("Enviar"):
    if not pergunta.strip():
        st.warning("Por favor, digite uma pergunta.")
    else:
        with st.spinner("⌛ Processando..."):
            body = {
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": [
                    {"role": "system", "content": "Você é um assistente útil que responde sempre em português."},
                    {"role": "user", "content": pergunta}
                ]
            }

            try:
                response = requests.post(url, headers=headers, data=json.dumps(body))
                response.raise_for_status()

                resposta = response.json()["choices"][0]["message"]["content"]
                st.success("Resposta da IA:")
                st.markdown(resposta)

            except requests.exceptions.HTTPError as e:
                st.error(f"❌ Erro HTTP {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"❌ Erro inesperado: {str(e)}")