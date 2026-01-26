import streamlit as st
from gradio_client import Client
import os
import shutil

# --- Page Config ---
st.set_page_config(page_title="AstraToonix Universal Voice", page_icon="🎙️")
st.title("🎙️ AstraToonix Voice (Multi-Server)")
st.info("अगर एक Server काम न करे, तो नीचे लिस्ट में से दूसरा नाम कॉपी करके पेस्ट करें।")

# --- Dynamic Space Input ---
# यहाँ यूजर खुद सर्वर बदल सकता है
space_id = st.text_input("Hugging Face Space ID:", value="fffiloni/xtts-v2-streaming")

st.markdown("""
**Try these Spaces if the default fails:**
1. `fffiloni/xtts-v2-streaming` (Best Public)
2. `ruslanmv/Text-To-Speech-XTTS` (Backup)
3. `kiv/xtts-v2` (Another Backup)
""")

# --- Inputs ---
text_input = st.text_area("Text (Hindi/English):", "नमस्ते राजदेव भाई! यह एक टेस्ट है।")
language = st.selectbox("Language", ["hi", "en"], index=0)
uploaded_file = st.file_uploader("Reference Audio (5-10s)", type=['wav', 'mp3', 'm4a'])

# --- Generation ---
if st.button("Generate Voice 🚀", type="primary"):
    if not uploaded_file:
        st.warning("⚠️ Please upload an audio file first.")
    else:
        status = st.empty()
        bar = st.progress(0)
        
        try:
            # Step A: File Setup
            status.text("Processing Audio...")
            ext = os.path.splitext(uploaded_file.name)[1]
            if not ext: ext = ".wav"
            temp_filename = f"temp_ref{ext}"
            
            with open(temp_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Step B: Connect to Chosen Space
            status.text(f"Connecting to {space_id}...")
            bar.progress(30)
            
            # Connect without token (Public Spaces)
            client = Client(space_id)

            # Step C: Generate
            status.text("Generating... (Waiting for GPU)")
            bar.progress(50)
            
            # Note: fffiloni space api parameters might differ slightly, 
            # but usually they follow the standard XTTS pattern.
            result = client.predict(
                text_input,      # Text
                language,        # Language
                temp_filename,   # Reference Audio
                temp_filename,   # Mic Audio
                False,           # Use Mic
                False,           # Cleanup
                True,            # Auto-detect off
                True,            # Agree TOS
                fn_index=1
            )
            
            bar.progress(100)
            status.text("✅ Done!")
            
            st.success("Audio Generated:")
            st.audio(result[1], format='audio/wav')
            
            # Cleanup
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

        except Exception as e:
            st.error("❌ Error occurred:")
            st.code(f"{e}")
            st.warning("Tip: ऊपर दिए गए 'Space ID' को बदलकर लिस्ट में से दूसरा नाम (जैसे 'ruslanmv/Text-To-Speech-XTTS') डालें और फिर बटन दबाएं।")
            
