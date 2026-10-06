import streamlit as st
import warnings
import os
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=DeprecationWarning)
load_dotenv()

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from core.rag_engine import build_rag_chain, ask_question


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="VoxMind — AI Video Assistant",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #080b12;
    --panel: #101521;
    --panel-2: #151b2a;
    --border: rgba(255,255,255,.09);
    --text: #f5f7fb;
    --muted: #8e98aa;
    --accent: #8b5cf6;
    --accent-2: #22d3ee;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(139,92,246,.13), transparent 30%),
        radial-gradient(circle at 85% 10%, rgba(34,211,238,.08), transparent 28%),
        var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
    background: rgba(10,13,21,.96);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

.brand {
    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom: 2rem;
}

.brand-mark {
    width:42px;
    height:42px;
    border-radius:13px;
    display:flex;
    align-items:center;
    justify-content:center;
    background: linear-gradient(135deg, #8b5cf6, #22d3ee);
    color:white;
    font-family:'Space Grotesk';
    font-size:22px;
    font-weight:700;
    box-shadow:0 10px 30px rgba(139,92,246,.25);
}

.brand-name {
    font-family:'Space Grotesk';
    font-size:20px;
    font-weight:700;
}

.brand-sub {
    color:var(--muted);
    font-size:11px;
    margin-top:2px;
}

.hero {
    padding: 28px 30px;
    border:1px solid var(--border);
    border-radius:24px;
    background:
        linear-gradient(135deg, rgba(139,92,246,.13), rgba(34,211,238,.04)),
        rgba(16,21,33,.85);
    box-shadow: 0 25px 80px rgba(0,0,0,.20);
    margin-bottom:22px;
}

.eyebrow {
    color:#a78bfa;
    text-transform:uppercase;
    letter-spacing:2px;
    font-size:11px;
    font-weight:700;
}

.hero h1 {
    font-family:'Space Grotesk';
    font-size:42px;
    line-height:1.05;
    margin:8px 0 10px;
    color:white;
}

.hero p {
    color:#a9b2c3;
    max-width:760px;
    font-size:15px;
    line-height:1.65;
    margin:0;
}

.card {
    background:rgba(16,21,33,.78);
    border:1px solid var(--border);
    border-radius:18px;
    padding:20px;
    margin-bottom:16px;
}

.card-title {
    font-family:'Space Grotesk';
    font-weight:600;
    font-size:17px;
    margin-bottom:8px;
}

.card-label {
    color:#8e98aa;
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:1px;
    margin-bottom:5px;
}

.metric-row {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:12px;
    margin-bottom:18px;
}

.metric {
    background:rgba(255,255,255,.025);
    border:1px solid var(--border);
    border-radius:15px;
    padding:15px;
}

.metric strong {
    display:block;
    font-family:'Space Grotesk';
    font-size:24px;
}

.metric span {
    color:var(--muted);
    font-size:12px;
}

.badge {
    display:inline-block;
    padding:5px 10px;
    border-radius:999px;
    background:rgba(139,92,246,.13);
    color:#c4b5fd;
    border:1px solid rgba(139,92,246,.2);
    font-size:11px;
    margin-right:6px;
}

.result-title {
    font-family:'Space Grotesk';
    font-size:28px;
    font-weight:700;
    margin:10px 0 16px;
}

.empty {
    text-align:center;
    padding:55px 20px;
    border:1px dashed rgba(255,255,255,.12);
    border-radius:20px;
    color:var(--muted);
}

.empty-icon {
    font-size:36px;
    margin-bottom:10px;
}

.chat-user {
    background:rgba(139,92,246,.12);
    border:1px solid rgba(139,92,246,.18);
    border-radius:16px;
    padding:12px 15px;
    margin:8px 0;
}

.chat-ai {
    background:rgba(34,211,238,.06);
    border:1px solid rgba(34,211,238,.12);
    border-radius:16px;
    padding:12px 15px;
    margin:8px 0 18px;
}

.small-muted {
    color:var(--muted);
    font-size:12px;
}

div.stButton > button {
    border-radius:12px;
    border:1px solid var(--border);
    background:#151b2a;
    color:white;
    font-weight:600;
    min-height:42px;
}

div.stButton > button:hover {
    border-color:rgba(139,92,246,.6);
    color:#c4b5fd;
}

div[data-testid="stFileUploader"] {
    border:1px dashed rgba(139,92,246,.35);
    border-radius:18px;
    padding:8px;
    background:rgba(139,92,246,.035);
}

.stTextInput input {
    border-radius:12px !important;
}

@media (max-width: 900px) {
    .hero h1 { font-size:32px; }
    .metric-row { grid-template-columns:1fr; }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def process_uploaded_file(uploaded_file):
    os.makedirs("uploads", exist_ok=True)
    path = os.path.join("uploads", uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path


def run_pipeline(source: str, language: str):
    with st.status("Building your AI meeting workspace...", expanded=True) as status:
        st.write("🎧 Processing audio...")
        chunks = process_input(source)

        st.write("📝 Transcribing audio...")
        transcript = transcribe_all(chunks, language=language)

        st.write("✨ Generating title...")
        title = generate_title(transcript)

        st.write("📋 Creating meeting summary...")
        summary = summarize(transcript)

        st.write("✅ Extracting action items...")
        action_items = extract_action_items(transcript)

        st.write("🔑 Extracting key decisions...")
        decisions = extract_key_decisions(transcript)

        st.write("❓ Finding open questions...")
        questions = extract_questions(transcript)

        st.write("🧠 Building semantic search index...")
        rag_chain = build_rag_chain(transcript)

        status.update(
            label="Your meeting workspace is ready",
            state="complete",
            expanded=False,
        )

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
        "source": source,
        "language": language,
    }


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">◈</div>
            <div>
                <div class="brand-name">VoxMind</div>
                <div class="brand-sub">AI VIDEO ASSISTANT</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Create workspace")

    source_mode = st.radio(
        "Source",
        ["YouTube / URL", "Upload file"],
        label_visibility="collapsed",
    )

    source = None

    if source_mode == "YouTube / URL":
        source = st.text_input(
            "Video URL",
            placeholder="Paste a YouTube URL...",
        )
    else:
        uploaded = st.file_uploader(
            "Upload video or audio",
            type=[
                "mp4", "mkv", "mov", "avi",
                "webm", "mp3", "wav", "m4a"
            ],
            label_visibility="collapsed",
        )
        if uploaded:
            source = process_uploaded_file(uploaded)

    language = st.selectbox(
        "Transcript language",
        ["english", "hinglish"],
        format_func=lambda x: "English" if x == "english" else "Hinglish → English",
    )

    process_clicked = st.button(
        "✦ Analyze video",
        use_container_width=True,
        type="primary",
    )

    st.divider()

    st.markdown(
        """
        <div class="small-muted">
        <b>Pipeline</b><br><br>
        Whisper / Sarvam → Transcript<br>
        Gemini → Insights<br>
        MiniLM → Embeddings<br>
        ChromaDB → RAG Chat
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.get("meeting"):
        if st.button("＋ New meeting", use_container_width=True):
            st.session_state.pop("meeting", None)
            st.session_state.pop("messages", None)
            st.rerun()


# ============================================================
# PROCESS
# ============================================================

if process_clicked:
    if not source:
        st.warning("Please provide a YouTube URL or upload a file.")
    else:
        try:
            st.session_state["meeting"] = run_pipeline(
                source,
                language,
            )
            st.session_state["messages"] = []
            st.rerun()
        except Exception as e:
            st.error(f"Something went wrong: {e}")


# ============================================================
# MAIN
# ============================================================

meeting = st.session_state.get("meeting")

if not meeting:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Your second brain for video</div>
            <h1>Turn long videos into<br>answers, insights & action.</h1>
            <p>
                Drop in a YouTube video or upload a recording.
                VoxMind transcribes it, understands the content,
                extracts what matters, and lets you chat with the
                entire conversation using RAG.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">01 · Understand</div>
                <div class="small-muted">
                    GPU-powered Whisper transcription or Sarvam
                    translation for Hinglish content.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">02 · Extract</div>
                <div class="small-muted">
                    Automatically surface summaries, action items,
                    decisions and unanswered questions.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">03 · Ask</div>
                <div class="small-muted">
                    Search the transcript semantically and ask
                    grounded questions with your RAG assistant.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="empty">
            <div class="empty-icon">◈</div>
            <b>Your workspace is waiting</b><br>
            <span>Paste a URL or upload a recording from the sidebar.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    title = meeting["title"] or "Untitled video"

    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">Analysis complete</div>
            <div class="result-title">{title}</div>
            <span class="badge">{meeting["language"].title()}</span>
            <span class="badge">RAG enabled</span>
            <span class="badge">AI analyzed</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_overview, tab_transcript, tab_chat = st.tabs(
        ["✦ Overview", "▤ Transcript", "⌕ Ask the meeting"]
    )

    # --------------------------------------------------------
    # OVERVIEW
    # --------------------------------------------------------

    with tab_overview:
        word_count = len(meeting["transcript"].split())

        st.markdown(
            f"""
            <div class="metric-row">
                <div class="metric">
                    <strong>{word_count:,}</strong>
                    <span>Transcript words</span>
                </div>
                <div class="metric">
                    <strong>{meeting["language"].title()}</strong>
                    <span>Processing mode</span>
                </div>
                <div class="metric">
                    <strong>RAG</strong>
                    <span>Knowledge engine</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        left, right = st.columns([1.25, 1])

        with left:
            st.markdown(
                '<div class="card-title">📋 Executive summary</div>',
                unsafe_allow_html=True,
            )
            st.markdown(meeting["summary"])

            st.markdown(
                '<div class="card-title" style="margin-top:25px;">✅ Action items</div>',
                unsafe_allow_html=True,
            )
            st.markdown(meeting["action_items"])

        with right:
            st.markdown(
                '<div class="card-title">🔑 Key decisions</div>',
                unsafe_allow_html=True,
            )
            st.markdown(meeting["key_decisions"])

            st.markdown(
                '<div class="card-title" style="margin-top:25px;">❓ Open questions</div>',
                unsafe_allow_html=True,
            )
            st.markdown(meeting["open_questions"])

    # --------------------------------------------------------
    # TRANSCRIPT
    # --------------------------------------------------------

    with tab_transcript:
        st.markdown(
            '<div class="card-title">Full transcript</div>',
            unsafe_allow_html=True,
        )

        st.text_area(
            "Transcript",
            value=meeting["transcript"],
            height=620,
            label_visibility="collapsed",
        )

    # --------------------------------------------------------
    # CHAT
    # --------------------------------------------------------

    with tab_chat:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Ask anything about this video</div>
                <div class="small-muted">
                    Answers are grounded in the indexed transcript.
                    Try asking about decisions, people, dates, explanations,
                    or specific moments.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        for msg in st.session_state["messages"]:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="chat-user"><b>You</b><br>{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="chat-ai"><b>VoxMind</b><br>{msg["content"]}</div>',
                    unsafe_allow_html=True,
                )

        question = st.chat_input(
            "Ask a question about the video..."
        )

        if question:
            st.session_state["messages"].append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            with st.spinner("Searching the meeting..."):
                answer = ask_question(
                    meeting["rag_chain"],
                    question,
                )

            st.session_state["messages"].append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            st.rerun()