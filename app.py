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
st.info("Note: This uses Coqui XTTS v2 via Hugging Face. It requires a Reference Audio for cloning.")

# --- 3. Environment Variable Check ---
hf_token = os.environ.get("HF_TOKEN")

if not hf_token:
    st.error("⚠️ Error: 'HF_TOKEN' Environment Variable not found in Koyeb Settings!")
    st.stop()

# --- 4. User Inputs ---
# Input Text
text_input = st.text_area(
    "Enter Text (Hindi/English):", 
    "नमस्ते राजदेव भाई, AstraToonix चैनल पर आपका स्वागत है!",
    height=100
)

# Language Selection
language = st.selectbox("Language", ["hi", "en"], index=0, format_func=lambda x: "Hindi" if x == "hi" else "English")

# Reference Audio Upload
uploaded_file = st.file_uploader("Upload Reference Audio (WAV/MP3, 5-10 sec)", type=['wav', 'mp3'])

# --- 5. Logic to Generate Audio ---
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
            
            with open("temp_ref.wav", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Step B: Connect to Hugging Face
            status_text.text("Connecting to AI Model (Coqui XTTS v2)...")
            status_bar.progress(40)
            
            client = Client("https://coqui-xtts-v2.hf.space/", hf_token=hf_token)

            # Step C: Send Request (This takes time)
            status_text.text("Generating Voice... (Please wait 30-60 seconds)")
            status_bar.progress(60)
            
            # API Parameters for XTTS v2
            result = client.predict(
                text_input,      # Text
                language,        # Language
                "temp_ref.wav",  # Reference Audio
                "temp_ref.wav",  # Mic Audio (Use same)
                False,           # Use Mic (False)
                False,           # Cleanup (False)
                True,            # Do not use auto-detect
                True,            # Agree to TOS
                fn_index=1       # Function index for generation
            )
            
            status_bar.progress(90)
            
            # Step D: Process Result
            audio_path = result[1] # Path to generated file
            
            # Display Success
            status_text.text("✅ Done! Audio Generated.")
            status_bar.progress(100)
            
            st.success("Your AI Audio is ready:")
            st.audio(audio_path, format='audio/wav')
            
            # Cleanup
            if os.path.exists("temp_ref.wav"):
                os.remove("temp_ref.wav")

        except Exception as e:
            status_bar.empty()
            st.error(f"❌ Error occurred: {e}")
            st.warning("Tip: If you see a 'Queue' error, the server is busy. Try again in 1 minute.")
          
