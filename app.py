import streamlit as st
import requests
import json

# --- UI DESIGN (Modern, Dark, Rounded) ---
st.set_page_config(page_title="AI Multi-Hub", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stChatMessage { 
        border-radius: 20px !important; 
        padding: 15px; 
        margin-bottom: 15px;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stChatInputContainer { border-radius: 30px !important; }
    .stSelectbox div[data-baseweb="select"] { border-radius: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- KONFIGURATION ---
# Ersetze die 111 durch deinen OpenRouter Key
API_KEY = "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"

MODELS = {
    "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
    "GPT-4o": "openai/gpt-4o",
    "Grok Beta": "x-ai/grok-beta",
    "Mistral Large": "mistralai/mistral-large",
    "Llama 3.1 (Free)": "meta-llama/llama-3.1-8b-instruct:free"
}

# --- LOGIK ---
st.title("🧠 AI Multi-Hub")
st.caption("Ein Interface für alle führenden KI-Modelle")

with st.sidebar:
    st.header("Optionen")
    selected_model = st.selectbox("Wähle ein Modell:", list(MODELS.keys()))
    if st.button("Chat löschen"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Schreibe eine Nachricht..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("KI denkt nach..."):
            try:
                # Der Server-Call (Umgeht die CORS-Sperre des Browsers)
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json",
                    },
                    data=json.dumps({
                        "model": MODELS[selected_model],
                        "messages": st.session_state.messages
                    })
                )
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Fehler: Bitte überprüfe deinen API-Key.")
            except Exception as e:
                st.error(f"Verbindung zum Server fehlgeschlagen.")
