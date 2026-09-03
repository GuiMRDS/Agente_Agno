import json
import requests
import streamlit as st

#  python -m streamlit run src/agente_agno/app.py

# =====================================================
# CONFIG
# =====================================================

AGENT_ID = "server-agente"
ENDPOINT_URL = f"http://localhost:8000/agents/{AGENT_ID}/runs"

st.set_page_config(
    page_title="Agente AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.block-container{
    max-width: 1100px;
}

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:700;
    margin-bottom:5px;
}

.sub-title{
    text-align:center;
    color:gray;
    margin-bottom:30px;
}

.stChatMessage{
    border-radius:16px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "events" not in st.session_state:
    st.session_state.events = []

# =====================================================
# API
# =====================================================

def get_response_stream(message: str):

    files_data = {
        "message": (None, message),
        "stream": (None, "true")
    }

    if st.session_state.session_id:
        files_data["session_id"] = (
            None,
            st.session_state.session_id
        )

    response = requests.post(
        ENDPOINT_URL,
        files=files_data,
        stream=True
    )

    if response.status_code != 200:
        raise Exception(response.text)

    for line in response.iter_lines():

        if not line:
            continue

        if line.startswith(b"data: "):
            try:
                yield json.loads(line[6:])
            except json.JSONDecodeError:
                pass

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("⚙️ Agente AI")

    st.success(f"Agente: {AGENT_ID}")

    st.divider()

    if st.button(
        "🗑️ Limpar Conversa",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.events = []
        st.session_state.session_id = None
        st.rerun()

    st.divider()

    total_chars = sum(
        len(msg["content"])
        for msg in st.session_state.messages
    )

    st.metric(
        "Mensagens",
        len(st.session_state.messages)
    )

    st.metric(
        "Caracteres",
        total_chars
    )

    st.divider()

    conversation_json = json.dumps(
        st.session_state.messages,
        ensure_ascii=False,
        indent=2
    )

    st.download_button(
        "📥 Exportar Conversa",
        conversation_json,
        file_name="conversa.json",
        use_container_width=True
    )

    st.divider()

    with st.expander("🔧 Últimos Eventos"):

        if st.session_state.events:
            st.json(
                st.session_state.events[-5:]
            )

# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div class="main-title">🤖 Agente AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Assistente criada com Agno + Groq</div>',
    unsafe_allow_html=True
)

# =====================================================
# HISTÓRICO
# =====================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# =====================================================
# CHAT INPUT
# =====================================================

if prompt := st.chat_input(
    "Digite sua mensagem..."
):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        full_response = ""

        with st.status(
            "🤖 Agente está pensando...",
            expanded=False
        ) as status:

            for event in get_response_stream(prompt):

                st.session_state.events.append(event)

                event_type = event.get("event")

                # Session
                if event_type == "RunStarted":

                    st.session_state.session_id = (
                        event.get("session_id")
                    )

                # Tool
                elif event_type == "ToolCallStarted":

                    tool = event.get("tool", {})

                    st.info(
                        f"🔧 Executando ferramenta: "
                        f"{tool.get('tool_name', 'Unknown')}"
                    )

                # Streaming
                elif event_type == "RunContent":

                    content = event.get(
                        "content",
                        ""
                    )

                    if content:
                        full_response += content

                        placeholder.markdown(
                            full_response + "▌"
                        )

                # Finalização
                elif event_type == "RunCompleted":

                    status.update(
                        label="✅ Resposta concluída",
                        state="complete"
                    )

        placeholder.markdown(full_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })