import streamlit as st
import edge_tts
import asyncio
import io  # Ye memory (RAM) handle karne ke liye hai

# --- Page Config ---
st.set_page_config(page_title="AstraToonix Studio", page_icon="🎙️")

# --- Session State (Memory) ---
if "audio_buffer" not in st.session_state:
    st.session_state.audio_buffer = None

# --- 1. TITLE & DISCLAIMER ---
st.title("AstraToonix")
st.caption("Welcome to Raj Audio Studio | RAM Mode (Fast & Error Free)")

st.warning("""
⚠️ **जरूरी सूचना:**
* Hindi Voice के लिए **हिंदी शब्द** ही लिखें।
* English Voice के लिए **English** लिखें।
""")

# --- 2. VOICE LIST ---
voice_options = {
    "🇮🇳 Hindi - Rajdev (Male)": "hi-IN-MadhurNeural",
    "🇮🇳 Hindi - Swara (Female)": "hi-IN-SwaraNeural",
    "🇮🇳 English (India) - Prabhat (Male)": "en-IN-PrabhatNeural",
    "🇮🇳 English (India) - Neerja (Female)": "en-IN-NeerjaNeural",
    "🇺🇸 English (US) - Christopher (Movie Guy)": "en-US-ChristopherNeural",
    "🇺🇸 English (US) - Guy (Standard Male)": "en-US-GuyNeural",
    "🇺🇸 English (US) - Jenny (Standard Female)": "en-US-JennyNeural",
    "🇺🇸 English (US) - Aria (Energetic)": "en-US-AriaNeural",
    "🇺🇸 English (US) - Ana (Child Voice)": "en-US-AnaNeural",
    "🇬🇧 English (UK) - Ryan (Male)": "en-GB-RyanNeural",
    "🇬🇧 English (UK) - Sonia (Female)": "en-GB-SoniaNeural",
    "🇺🇸 English (US) - Eric (Heavy Male)": "en-US-EricNeural"
}

selected_voice_name = st.selectbox("Select Voice (Character):", list(voice_options.keys()))
selected_voice_code = voice_options[selected_voice_name]

# --- 3. SLIDERS ---
col1, col2 = st.columns(2)
with col1:
    rate_val = st.slider("Speed (Flow)", -50, 50, 10, format="%d%%")
    rate_str = f"{rate_val:+d}%"

with col2:
    pitch_val = st.slider("Pitch (Tone)", -20, 20, -2, format="%dHz")
    pitch_str = f"{pitch_val:+d}Hz"

# --- 4. SCRIPT INPUT ---
st.markdown("### Script:")
default_text = """नमस्ते दोस्तों! मेरा नाम है राजदेव।
मैं क्रिएटर हूँ AstraToonix का!
कोडिंग मेरा दिमाग है, लेकिन AstraToonix मेरा दिल है।"""

text_input = st.text_area("Yahan likhein:", default_text, height=200)

# --- 5. LOGIC (RAM MODE - NO FILE SAVING) ---
async def generate_audio_in_memory(text, v_code, rate, pitch):
    clean_text = text.replace("\n", " ")
    communicate = edge_tts.Communicate(clean_text, v_code, rate=rate, pitch=pitch)
    
    # Hum file save nahi karenge, sidha bytes (data) collect karenge
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
            
    return audio_data

# --- GENERATE BUTTON ---
if st.button("Generate Audio 🎧", type="primary"):
    if not text_input:
        st.warning("Script khali hai!")
    else:
        status = st.empty()
        status.text("Generating...")
        
        try:
            # 1. RAM me audio generate karo
            audio_bytes = asyncio.run(generate_audio_in_memory(text_input, selected_voice_code, rate_str, pitch_str))
            
            if len(audio_bytes) > 0:
                # 2. Session State me save karo
                st.session_state.audio_buffer = audio_bytes
                status.text("✅ Done!")
            else:
                status.error("❌ Audio generate hua par khali (0 bytes) hai. Dubara try karein.")
            
        except Exception as e:
            st.error(f"Error: {e}")

# --- RESULT SECTION ---
if st.session_state.audio_buffer is not None:
    st.success("Audio Ready!")
    
    # Audio Player (Memory se chalega)
    st.audio(st.session_state.audio_buffer, format='audio/mp3')
    
    # Download Button
    st.download_button(
        label="Download MP3 📥",
        data=st.session_state.audio_buffer,
        file_name="AstraToonix_Audio.mp3",
        mime="audio/mpeg"
    )
    
