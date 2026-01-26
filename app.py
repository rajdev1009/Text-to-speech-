import streamlit as st
from gradio_client import Client
import os
import shutil
import time

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="AstraToonix AI Voice",
    page_icon="🎙️",
    layout="centered"
)

# --- 2. Title and Branding ---
st.title("🎙️ AstraToonix AI Voice Generator")
st.markdown("### Create Realistic Voices for Comedy & Videos")
st.info("Note: Using 'tonyassi/xtts-v2' server. Ensure audio sample is clear.")

# --- 3. User Inputs ---
text_input = st.text_area(
    "Enter Text (Hindi/English):", 
    "नमस्ते राजदेव भाई, AstraToonix चैनल पर आपका स्वागत है!",
    height=100
)

# Language Selection
language = st.selectbox("Language", ["hi", "en"], index=0, format_func=lambda x: "Hindi" if x == "hi" else "English")

# Reference Audio Upload (M4A Support)
uploaded_file = st.file_uploader("Upload Reference Audio (WAV/MP3/M4A, 5-10 sec)", type=['wav', 'mp3', 'm4a'])

# --- 4. Logic to Generate Audio ---
if st.button("Generate Voice 🚀", type="primary"):
    if not uploaded_file:
        st.warning("⚠️ Please upload a reference audio file first!")
    elif not text_input:
        st.warning("⚠️ Please enter some text!")
    else:
        status_text = st.empty()
        status_bar = st.progress(0)
        
        try:
            # Step A: Save uploaded file temporarily
            status_text.text("Processing your reference audio...")
            status_bar.progress(20)
            
            # Detect extension
            file_extension = os.path.splitext(uploaded_file.name)[1]
            if not file_extension:
                file_extension = ".wav"
            
            temp_filename = f"temp_ref{file_extension}"
            
            with open(temp_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Step B: Connect to Hugging Face
            status_text.text("Connecting to AI Model (Server: tonyassi)...")
            status_bar.progress(40)
            
            # NEW SERVER ADDRESS (More Stable)
            client = Client("tonyassi/xtts-v2")

            # Step C: Send Request
            status_text.text("Generating Voice... (Please wait 30-60 seconds)")
            status_bar.progress(60)
            
            # API Parameters
            result = client.predict(
                text_input,      # Text
                language,        # Language
                temp_filename,   # Reference Audio
                temp_filename,   # Mic Audio
                False,           # Use Mic
                False,           # Cleanup
                False,           # Auto-detect off (updated param)
                True,            # Agree to TOS
                fn_index=0       # Updated index for this server
            )
            
            status_bar.progress(90)
            
            # Step D: Process Result
            audio_path = result[1] 
            
            # Display Success
            status_text.text("✅ Done! Audio Generated.")
            status_bar.progress(100)
            
            st.success("Your AI Audio is ready:")
            st.audio(audio_path, format='audio/wav')
            
            # Cleanup
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

        except Exception as e:
            status_bar.empty()
            st.error(f"❌ Error occurred: {e}")
            st.warning("Tip: Server might be busy. Wait 1 minute and try again.")
            
