import streamlit as st
import edge_tts
import asyncio
import os

# --- Page Config ---
st.set_page_config(page_title="AstraToonix Final", page_icon="✅")
st.title("✅ AstraToonix Final Studio")
st.caption("No Coding Errors | Pure Audio Flow")

# --- 1. Voice Setup ---
voice_options = {
    "Hindi - Rajdev (Male)": "hi-IN-MadhurNeural",
    "Hindi - Swara (Female)": "hi-IN-SwaraNeural",
    "English - Christopher": "en-US-ChristopherNeural"
}

selected_voice_name = st.selectbox("Select Voice:", list(voice_options.keys()))
selected_voice_code = voice_options[selected_voice_name]

# --- 2. Sliders (Direct Control) ---
col1, col2 = st.columns(2)
with col1:
    # Rate ko string format me convert karna zaroori hai
    rate_val = st.slider("Speed (Flow)", -50, 50, 10, format="%d%%")
    rate_str = f"{rate_val:+d}%"

with col2:
    pitch_val = st.slider("Pitch (Tone)", -20, 20, -2, format="%dHz")
    pitch_str = f"{pitch_val:+d}Hz"

# --- 3. Script Input ---
st.markdown("### Script:")
default_text = "नमस्ते राजदेव भाई! अब यह कोड बिल्कुल सही काम करेगा। न कोई एरर, न कोई फालतू बकवास।"
text_input = st.text_area("Yahan likhein:", default_text, height=150)

# --- 4. Logic Fix (Direct Parameters) ---
# Is function me hum koi SSML Code nahi banayenge.
# Hum seedha library ke features use karenge.

async def generate_audio(text, v_code, rate, pitch):
    # Newline fix for better flow
    clean_text = text.replace("\n", " ")
    
    # Communicate function me seedha rate aur pitch daalenge.
    # Ye sabse safe tareeka hai.
    communicate = edge_tts.Communicate(clean_text, v_code, rate=rate, pitch=pitch)
    
    output_file = "final_output.mp3"
    await communicate.save(output_file)
    return output_file

if st.button("Generate Audio 🎧", type="primary"):
    if not text_input:
        st.warning("Script khali hai!")
    else:
        status = st.empty()
        status.text("Generating...")
        
        try:
            # Async run
            output_path = asyncio.run(generate_audio(text_input, selected_voice_code, rate_str, pitch_str))
            
            status.text("✅ Done!")
            st.audio(output_path, format='audio/mp3')
            st.success(f"Generated with Speed: {rate_str} | Pitch: {pitch_str}")
            
        except Exception as e:
            st.error(f"Error: {e}")
            
