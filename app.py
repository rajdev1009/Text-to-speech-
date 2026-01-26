import streamlit as st
import edge_tts
import asyncio
import os

# --- Page Config ---
st.set_page_config(page_title="AstraToonix Voice Tuner", page_icon="🎚️")

st.title("🎚️ AstraToonix Voice Tuner")
st.markdown("### Create Unique Voices (Unlimited & Free)")
st.info("ℹ️ Since XTTS servers are down globally, we are using Neural Edge TTS with Pitch Control to create unique voices.")

# --- Inputs ---
text_input = st.text_area("Script (Hindi/English):", "नमस्ते राजदेव भाई! AstraToonix चैनल पर आपका स्वागत है।", height=100)

# Voice Selection
voice_options = {
    "Hindi - Swara (Female)": "hi-IN-SwaraNeural",
    "Hindi - Madhur (Male)": "hi-IN-MadhurNeural",
    "English - Christopher (Male)": "en-US-ChristopherNeural",
    "English - Aria (Female)": "en-US-AriaNeural",
    "English - Guy (Male)": "en-US-GuyNeural"
}
selected_voice_name = st.selectbox("Select Base Voice:", list(voice_options.keys()))
selected_voice_code = voice_options[selected_voice_name]

# --- 🎚️ The Magic Controls (To make it UNIQUE) ---
col1, col2 = st.columns(2)

with col1:
    # Rate: -50% (Slow) to +50% (Fast)
    rate_val = st.slider("Speaking Rate (Speed)", -50, 50, 0, format="%d%%")
    rate_str = f"{rate_val:+d}%"

with col2:
    # Pitch: -20Hz (Deep) to +20Hz (High/Chipmunk)
    pitch_val = st.slider("Pitch (Tone/Bhari-pan)", -20, 20, 0, format="%dHz")
    pitch_str = f"{pitch_val:+d}Hz"

# --- Generation Logic ---
async def generate_audio(text, voice, rate, pitch):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    output_file = "output_voice.mp3"
    await communicate.save(output_file)
    return output_file

if st.button("Generate Audio 🎧", type="primary"):
    if not text_input:
        st.warning("Please enter some text.")
    else:
        status = st.empty()
        status.text("Generating...")
        
        try:
            # Running the async function
            output_path = asyncio.run(generate_audio(text_input, selected_voice_code, rate_str, pitch_str))
            
            status.text("✅ Done!")
            st.audio(output_path, format='audio/mp3')
            
            st.success(f"Generated with Pitch: {pitch_str} | Rate: {rate_str}")
            
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Designed for AstraToonix | Runs smoothly on Koyeb Free Tier")
