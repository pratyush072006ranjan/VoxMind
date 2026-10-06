# ◈ VoxMind — AI Video Assistant

> **VoxMind** is a Streamlit-based AI video/audio assistant that converts long-form YouTube videos or uploaded recordings into searchable transcripts, summaries, action items, key decisions, open questions, and an interactive RAG-powered chat experience.

## ✨ Features

- 🎬 YouTube / URL input
- 📁 Local video/audio upload
- 🇬🇧 English transcription
- 🇮🇳 Hinglish → English processing
- 📋 AI-generated executive summary
- ✅ Action-item extraction
- 🔑 Key-decision extraction
- ❓ Open-question extraction
- 🧠 Transcript-based RAG
- 💬 Interactive chat with the analyzed video
- 📄 Full transcript view
- 📊 Transcript metrics
- 🎨 Dark cinematic Streamlit dashboard

The application imports audio processing, transcription, summarization, extraction, and RAG functionality from the project's `utils` and `core` modules. 

## 🧠 How It Works

```text
YouTube URL / Uploaded Media
            ↓
      Audio Processing
            ↓
       Transcription
            ↓
       AI Analysis
            ↓
   ┌────────┼─────────┐
   ↓        ↓         ↓
Summary  Decisions  Questions
   │
   └────────────┐
                ↓
          RAG Knowledge Base
                ↓
          Semantic Retrieval
                ↓
             AI Chat
```

The analysis pipeline processes audio, transcribes it, generates a title and summary, extracts action items, decisions and questions, and finally builds a RAG chain.

## 🏗️ Project Structure

```text
VoxMind/
│
├── app.py
│
├── core/
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── extractor.py
│   └── rag_engine.py
│
├── utils/
│   └── audio_processor.py
│
├── uploads/
│
├── .env
├── requirements.txt
└── README.md
```

### Main modules

`app.py` — Streamlit UI and application orchestration.

`utils/audio_processor.py` — Processes the supplied audio/video source.

`core/transcriber.py` — Transcribes processed audio.

`core/summarizer.py` — Generates the title and executive summary.

`core/extractor.py` — Extracts action items, key decisions and open questions.

`core/rag_engine.py` — Builds the RAG chain and answers questions about the transcript.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Streamlit | Web UI |
| Whisper / Sarvam | Transcription / translation |
| Gemini | AI insights |
| MiniLM | Embeddings |
| ChromaDB | Vector database |
| RAG | Transcript question answering |
| bgutil-ytdlp-pot-provider | YouTube processing support |
| python-dotenv | Environment variables |

The current application's sidebar describes the pipeline as Whisper/Sarvam → Transcript, Gemini → Insights, MiniLM → Embeddings, and ChromaDB → RAG Chat.

## ⚙️ Installation

### 1. Open the project

```powershell
cd "YOUR_VOXMIND_PROJECT_DIRECTORY"
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

If your environment already exists, simply activate it.

### 3. Install dependencies

If using `pip`:

```powershell
pip install -r requirements.txt
```

Or install the main Streamlit dependency:

```powershell
pip install streamlit
```

Use the project's existing `requirements.txt` for the remaining AI/audio dependencies.

## 🔑 Environment Variables

Create a `.env` file in the project root.

Add the API keys required by your `core` and `utils` modules. For example:

```env
GOOGLE_API_KEY=your_google_api_key
MISTRAL_API_KEY=your_mistral_api_key
```

If your implementation uses Sarvam or other services, add their required keys as well.

The application loads environment variables using:

```python
from dotenv import load_dotenv

load_dotenv()
```

**Never commit `.env` to GitHub.**

Recommended `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
uploads/
```

# ▶️ How to Run VoxMind

## ⚠️ Important: Use Two Terminals

For YouTube processing, your current setup requires the local:

```text
bgutil-ytdlp-pot-provider
```

server to be running first.

You should therefore start VoxMind using **two terminals**.

---

## 🟣 Terminal 1 — Start bgutil provider

Open **Terminal 1**.

Run:

```powershell
cd "$HOME\bgutil-ytdlp-pot-provider\server"
```

Then:

```powershell
node build/main.js
```

### Important

Keep this terminal running.

Do **not** close it while using YouTube URLs in VoxMind.

This starts the local provider required by the YouTube/yt-dlp processing workflow.

---

## 🟢 Terminal 2 — Start Streamlit

Open a **second terminal**.

Navigate to your VoxMind project:

```powershell
cd "YOUR_VOXMIND_PROJECT_DIRECTORY"
```

Then run:

```powershell
streamlit run app.py
```

If you use `uv`:

```powershell
uv run streamlit run app.py
```

Streamlit will display the local application URL in the terminal, normally similar to:

```text
http://localhost:8501
```

Open that URL in your browser.

---

## 🚀 Quick Start

### Terminal 1

```powershell
cd "$HOME\bgutil-ytdlp-pot-provider\server"
node build/main.js
```

Keep it running.

### Terminal 2

```powershell
cd "YOUR_VOXMIND_PROJECT_DIRECTORY"
streamlit run app.py
```

That's the complete startup process.

## 🎬 Using a YouTube Video

1. Start the bgutil provider in Terminal 1.
2. Start Streamlit in Terminal 2.
3. Open VoxMind.
4. Select:

```text
YouTube / URL
```

5. Paste your YouTube URL.
6. Select transcript language:
   - English
   - Hinglish → English
7. Click:

```text
✦ Analyze video
```

8. Wait for processing to finish.
9. Explore:
   - ✦ Overview
   - ▤ Transcript
   - ⌕ Ask the meeting

## 📁 Using a Local Video / Audio File

Select:

```text
Upload file
```

The current application accepts:

```text
.mp4
.mkv
.mov
.avi
.webm
.mp3
.wav
.m4a
```

Then:

```text
Upload
   ↓
Select language
   ↓
✦ Analyze video
   ↓
AI Processing
   ↓
Workspace Ready
```

Uploaded files are saved into the local `uploads/` directory before processing.

## 🔬 Processing Pipeline

When **Analyze video** is clicked:

```text
🎧 Processing audio
        ↓
📝 Transcribing audio
        ↓
✨ Generating title
        ↓
📋 Creating meeting summary
        ↓
✅ Extracting action items
        ↓
🔑 Extracting key decisions
        ↓
❓ Finding open questions
        ↓
🧠 Building semantic search index
        ↓
        READY
```

## 📊 Dashboard

After processing, VoxMind provides three main tabs:

### ✦ Overview

Displays:

- Transcript word count
- Processing mode
- RAG status
- Executive summary
- Action items
- Key decisions
- Open questions

### ▤ Transcript

Displays the full generated transcript.

### ⌕ Ask the meeting

Provides an interactive chat interface grounded in the indexed transcript.

Example questions:

```text
What is the main topic of this video?
```

```text
What decisions were made?
```

```text
What action items were assigned?
```

```text
What questions remained unanswered?
```

```text
Explain the discussion about the project.
```

## 🧠 RAG Architecture

```text
Transcript
    ↓
Embedding Model
    ↓
ChromaDB
    ↓
Retriever
    ↓
Relevant Transcript Chunks
    ↓
AI Model
    ↓
Grounded Answer
```

The RAG engine is provided by:

```python
build_rag_chain(transcript)
```

Questions are answered using:

```python
ask_question(
    meeting["rag_chain"],
    question
)
```

## 📁 Uploaded File Storage

Uploaded media is saved to:

```text
uploads/
```

The application creates this directory automatically.

If you process sensitive recordings, review your storage and cleanup policy before deploying the application publicly.

## 🔄 Development Workflow

Once Streamlit is running, saving Python changes normally triggers Streamlit's automatic rerun.

You generally do **not** need to manually restart Streamlit after every code change.

Keep Terminal 1 running if you are using YouTube processing.

## ⚠️ Troubleshooting

### YouTube processing does not work

Make sure Terminal 1 is running:

```powershell
cd "$HOME\bgutil-ytdlp-pot-provider\server"
node build/main.js
```

Then run Streamlit in Terminal 2:

```powershell
streamlit run app.py
```

### Streamlit command not found

Check:

```powershell
streamlit --version
```

If needed:

```powershell
pip install streamlit
```

### Node command does not work

Verify Node.js is installed:

```powershell
node --version
```

Then verify the provider build exists:

```text
$HOME\bgutil-ytdlp-pot-provider\server\build\main.js
```

### API errors

Check the `.env` file and verify that the required API keys are configured.

### Upload errors

Make sure the file extension is supported:

```text
mp4, mkv, mov, avi, webm, mp3, wav, m4a
```

## ⚠️ Current Limitations

- YouTube processing depends on the local bgutil provider being available.
- The provider must be started before YouTube-based processing.
- Long videos can take significant time to process.
- Transcription quality depends on audio quality and the selected transcription pipeline.
- AI-generated summaries and extracted insights can contain mistakes.
- Uploaded files are currently stored locally.
- RAG quality depends on transcript quality and the implementation in `rag_engine.py`.

## 🔮 Future Improvements

### 🎥 Timestamped Answers

Return references such as:

```text
The database decision was discussed around 14:32.
```

### 👥 Speaker Diarization

Identify different speakers:

```text
Speaker 1:
...

Speaker 2:
...
```

### 📚 Multi-Video RAG

Allow several videos to be indexed together:

```text
Video 1
Video 2
Video 3
    ↓
Unified RAG
    ↓
Cross-video questions
```

### 📊 Advanced Analytics

Add:

- Video duration
- Speaker count
- Speaking time
- Topic distribution
- Word count
- Processing time

### 📥 Export

Add downloads for:

- PDF summary
- Markdown
- TXT
- JSON
- Transcript

## 🔐 Security

Never hard-code API keys.

### ❌ Don't do this

```python
GOOGLE_API_KEY = "my-secret-key"
```

### ✅ Use `.env`

```env
GOOGLE_API_KEY=your_api_key
```

And load it with:

```python
from dotenv import load_dotenv

load_dotenv()
```

## 🤝 Contributing

1. Fork the repository.
2. Create a branch:

```bash
git checkout -b feature/new-feature
```

3. Make your changes.
4. Commit:

```bash
git commit -m "Add new feature"
```

5. Push:

```bash
git push origin feature/new-feature
```

6. Open a Pull Request.

## 📜 License

This project is intended for educational and development purposes.

Add an appropriate open-source license if you plan to distribute it publicly.

## 👨‍💻 Project

# VoxMind — AI Video Assistant

Built with:

**Python • Streamlit • Whisper/Sarvam • Gemini • MiniLM • ChromaDB • RAG**

> **"Don't watch everything. Understand everything." ◈**
