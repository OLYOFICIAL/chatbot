import pandas as pd
import streamlit as st

# Carregar planilha
file_path = "Duvidas Processos chatbot.xlsx"
df = pd.read_excel(file_path, sheet_name="Planilha1")

# Organizar dados
dados = {}
for _, row in df.iterrows():
    frente = row["Frente"]
    topico = row["Tópicos"]
    pergunta = row["Pergunta"]
    resposta = row["Resposta"]

    if frente not in dados:
        dados[frente] = {}
    if topico not in dados[frente]:
        dados[frente][topico] = []
    dados[frente][topico].append((pergunta, resposta))

# Configuração do app
st.set_page_config(page_title="Chatbot de Processos", layout="wide")
st.markdown("<h2 style='text-align:center;'>🤖 Chatbot de Processos</h2>", unsafe_allow_html=True)

# Inicializar histórico
if "messages" not in st.session_state:
    st.session_state.messages = []
if "nivel" not in st.session_state:
    st.session_state.nivel = "frente"   # frente → topico → pergunta
if "frente_atual" not in st.session_state:
    st.session_state.frente_atual = None
if "topico_atual" not in st.session_state:
    st.session_state.topico_atual = None

# Função para mostrar balões
def render_message(role, content):
    if role == "user":
        st.markdown(
            f"<div style='text-align:right; background:#DCF8C6; padding:10px; border-radius:15px; margin:5px; max-width:70%; float:right; clear:both;'>{content}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='text-align:left; background:#F1F0F0; padding:10px; border-radius:15px; margin:5px; max-width:70%; float:left; clear:both;'>{content}</div>",
            unsafe_allow_html=True,
        )

# Mostrar histórico
for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"])

st.markdown("<br><hr>", unsafe_allow_html=True)

# Fluxo de navegação estilo Copilot
if st.session_state.nivel == "frente":
    st.write("👉 Escolha uma **Frente de Processo**:")
    cols = st.columns(3)
    for i, frente in enumerate(dados.keys()):
        if cols[i % 3].button(frente):
            st.session_state.messages.append({"role": "user", "content": frente})
            st.session_state.frente_atual = frente
            st.session_state.nivel = "topico"
            st.rerun()

elif st.session_state.nivel == "topico":
    frente = st.session_state.frente_atual
    st.write(f"👉 Frente escolhida: **{frente}**\n\nSelecione um **Tópico**:")
    cols = st.columns(2)
    for i, topico in enumerate(dados[frente].keys()):
        if cols[i % 2].button(topico):
            st.session_state.messages.append({"role": "user", "content": topico})
            st.session_state.topico_atual = topico
            st.session_state.nivel = "pergunta"
            st.rerun()

elif st.session_state.nivel == "pergunta":
    frente = st.session_state.frente_atual
    topico = st.session_state.topico_atual
    st.write(f"👉 Tópico escolhido: **{topico}**\n\nEscolha uma **Pergunta**:")
    for pergunta, resposta in dados[frente][topico]:
        if st.button(pergunta):
            st.session_state.messages.append({"role": "user", "content": pergunta})
            st.session_state.messages.append({"role": "bot", "content": resposta})
            st.session_state.nivel = "pergunta"  # continua no mesmo nível
            st.rerun()

# Botão reset
if st.button("🔄 Reiniciar Conversa"):
    st.session_state.clear()
    st.rerun()
