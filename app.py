import streamlit as st
import subprocess
import os
import sys

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="AI YouTube Bot",
    page_icon="🎬",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main {background-color: #0a0a1a;}
    .stButton>button {
        background-color: #ff6b00;
        color: white;
        font-size: 20px;
        padding: 15px 40px;
        border-radius: 10px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ff8c00;
    }
    .title {
        font-size: 50px;
        font-weight: bold;
        color: #ffc800;
        text-align: center;
    }
    .subtitle {
        font-size: 20px;
        color: #aaaaff;
        text-align: center;
    }
    .step-box {
        background-color: #1a1a2e;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ffc800;
        margin: 10px 0;
    }
    .success-box {
        background-color: #0a2e0a;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00ff00;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown('<p class="title">🤖 AI YouTube Channel Bot</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Fully Automated • Open Source • No Paid APIs</p>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# TECH STACK BADGES
# ============================================================
col1, col2, col3, col4, col5 = st.columns(5)
col1.success("🧠 Ollama + Llama3")
col2.info("🎙️ Coqui TTS")
col3.warning("📝 Whisper")
col4.error("🎬 FFmpeg")
col5.success("🖼️ Pillow")

st.markdown("---")

# ============================================================
# PIPELINE STATUS
# ============================================================
st.markdown("## 🚀 Pipeline Control")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### ⚙️ Settings")
    topic = st.text_input(
        "📌 Video Topic",
        value="5 Unsolved History Mysteries That Will Shock You",
        help="Enter the topic for your YouTube video"
    )

    voice_model = st.selectbox(
        "🎙️ Voice Model",
        ["VITS (High Quality)", "Tacotron2 (Fast)"],
        help="Select the TTS model for voice generation"
    )

    st.markdown("### 📋 Pipeline Steps")
    st.markdown("""
    <div class="step-box">✅ Step 1 — AI Script Generation (Ollama + Llama3)</div>
    <div class="step-box">✅ Step 2 — Voice Generation (Coqui TTS)</div>
    <div class="step-box">✅ Step 3 — Subtitle Generation (Whisper)</div>
    <div class="step-box">✅ Step 4 — Thumbnail Creation (Pillow)</div>
    <div class="step-box">✅ Step 5 — Video Assembly (FFmpeg)</div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("### 📁 Output Files")

    files = {
        "script.txt": "📄 AI Generated Script",
        "voiceover.wav": "🎙️ AI Voiceover",
        "subtitles.srt": "📝 Subtitles",
        "thumbnail.png": "🖼️ Thumbnail",
        "final_video.mp4": "🎬 Final Video"
    }

    for filename, label in files.items():
        if os.path.exists(filename):
            st.success(f"✅ {label} — Ready")
        else:
            st.error(f"⏳ {label} — Not generated yet")

    st.markdown("### 🎬 Preview")
    if os.path.exists("thumbnail.png"):
        st.image("thumbnail.png", caption="Generated Thumbnail", use_column_width=True)

st.markdown("---")

# ============================================================
# RUN BUTTON
# ============================================================
st.markdown("## ▶️ Run Pipeline")
st.warning("⚠️ Make sure Ollama is running in background before clicking Run!")

if st.button("🚀 Generate YouTube Video Now!"):
    st.markdown("### 📊 Pipeline Running...")

    progress = st.progress(0)
    status = st.empty()

    steps = [
        (10, "🧠 Generating script with Ollama + Llama3..."),
        (30, "🎙️ Generating voiceover with Coqui TTS..."),
        (50, "📝 Generating subtitles with Whisper..."),
        (70, "🖼️ Creating thumbnail with Pillow..."),
        (85, "🎬 Creating video frames..."),
        (95, "⚙️ Assembling final video with FFmpeg..."),
        (100, "✅ Pipeline Complete!")
    ]

    for pct, msg in steps:
        progress.progress(pct)
        status.info(msg)

    # Run actual pipeline
    result = subprocess.run(
        [sys.executable, "pipeline.py"],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

    if result.returncode == 0:
        st.balloons()
        st.success("🎉 Pipeline completed successfully!")
        st.markdown("### 📁 Generated Files")
        for filename, label in files.items():
            if os.path.exists(filename):
                st.success(f"✅ {label}")
        if os.path.exists("thumbnail.png"):
            st.image("thumbnail.png", caption="Generated Thumbnail")
        if os.path.exists("final_video.mp4"):
            st.success("🎬 final_video.mp4 is ready! Open your project folder to watch it.")
    else:
        st.error("❌ Pipeline failed. Check terminal for errors.")
        st.code(result.stderr)

st.markdown("---")

# ============================================================
# ARCHITECTURE DIAGRAM
# ============================================================
st.markdown("## 🏗️ System Architecture")
st.markdown("""""")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<p style='text-align:center; color:#666'>
Built with ❤️ using Ollama • Coqui TTS • Whisper • FFmpeg • Streamlit<br>
Fully Open Source • No Paid APIs • TruBot AI Assignment
</p>
""", unsafe_allow_html=True)