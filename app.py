import streamlit as st
from gradio_client import Client
import os
import shutil

# --- 1. Page Config ---
st.set_page_config(page_title="AstraToonix Voice 2026", page_icon="🎙️")
st.title("🎙️ AstraToonix Voice Generator (No Token Needed)")
st.info("Using Public Space: Deep50D/XTTS_V2_CPU_fixed")

# --- 2. Inputs ---
text_input = st.text_area("Text (Hindi/English):", "नमस्ते राजदेव भाई! AstraToonix में आपका स्वागत है।")
language = st.selectbox("Language", ["hi", "en"], index=0)
uploaded_file = st.file_uploader("Reference Audio (5-10s)", type=['wav', 'mp3', 'm4a'])

# --- 3. Generation ---
if st.button("Generate Voice 🚀", type="primary"):
    if not uploaded_file:
        st.warning("⚠️ Please upload an audio file first.")
    else:
        status = st.empty()
        bar = st.progress(0)
        
        try:
            # Step A: File Setup
            status.text("Processing Audio...")
            # Extension handle karna
            ext = os.path.splitext(uploaded_file.name)[1]
            if not ext: ext = ".wav"
            temp_filename = f"temp_ref{ext}"
            
            with open(temp_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Step B: Connect to Public Space (NO TOKEN NEEDED)
            status.text("Connecting to Public Server...")
            bar.progress(30)
            
            # यह एक Public Space है, इसलिए hf_token की जरूरत नहीं
            client = Client("Deep50D/XTTS_V2_CPU_fixed")

            # Step C: Generate
            status.text("Generating... (Might take 1-2 mins on CPU)")
            bar.progress(50)
            
            # API Call (Parameters for this specific space)
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
            st.error("❌ Error:")
            st.code(f"{e}")
            st.warning("Tip: Since this is a Free CPU Space, it might be slow. Be patient.")

