import streamlit as st
import edge_tts
import asyncio
import os

# --- Page Config ---
st.set_page_config(page_title="AstraToonix Studio", page_icon="🎚️")
st.title("🎚️ AstraToonix Pro Studio (Rajdev Edition)")
st.caption("Custom Pitch + Speed + Human Flow Logic")

# --- 1. Voice Setup (Naam Change kar diya) ---
voice_options = {
    "Hindi - Rajdev (Male)": "hi-IN-MadhurNeural",  # Yahan Madhur ko Rajdev bana diya
    "Hindi - Swara (Female)": "hi-IN-SwaraNeural",
    "English - Christopher": "en-US-ChristopherNeural"
}

# Dropdown me ab "Rajdev" dikhega
selected_voice_name = st.selectbox("Select Voice:", list(voice_options.keys()))
selected_voice_code = voice_options[selected_voice_name]

# --- 2. Manual Controls (Sliders Wapas aa gaye) ---
col1, col2 = st.columns(2)

with col1:
    # Speed Control
    rate_val = st.slider("Global Speed (Rate)", -50, 50, 10, format="%d%%") # Default +10% for flow
    rate_str = f"{rate_val:+d}%"

with col2:
    # Pitch Control (Awaaz ka bhari-pan)
    pitch_val = st.slider("Global Pitch (Tone)", -20, 20, -2, format="%dHz") # Default -2Hz
    pitch_str = f"{pitch_val:+d}Hz"

# --- 3. Input & Help ---
st.markdown("### Script Editor:")
default_text = """अरे भाई क्या हाल है? [laugh]
आज तो मजा ही आ गया यार! [happy]
तुम वहाँ क्यों खड़े हो? [angry] जल्दी इधर आओ!"""

text_input = st.text_area("Yahan likhein:", default_text, height=150)

st.markdown("""
**Magic Tags (Script me use karein):**
* `[laugh]` = Hasi (Ha ha ha)
* `[happy]` = Khushi/Josh wala Sur
* `[angry]` = Gussa/Bhari Awaaz
""")

# --- 4. The "Humanizer" Logic ---
def humanize_text(text):
    # Newlines remove to fix pauses
    text = text.replace("\n", " ")
    
    # Laughter
    laugh_sound = '<prosody rate="+50%" pitch="+20Hz" volume="+20%">हहाहाहाहाहा</prosody>' 
    text = text.replace("[laugh]", laugh_sound)
    
    # Happy Flow (Override Global settings temporarily)
    text = text.replace("[happy]", '<prosody rate="+20%" pitch="+10Hz">')
    
    # Angry Flow
    text = text.replace("[angry]", '<prosody rate="+0%" pitch="-15Hz">')
    
    # Reset Tags
    if "[happy]" in text or "[angry]" in text:
        text = text + "</prosody>"
        
    return text

# --- 5. Generation ---
async def generate_audio(text, v_code, rate, pitch):
    # Step A: Humanize (Tags process karna)
    final_text = humanize_text(text)
    
    # Step B: Generate with Global Sliders
    # Note: Tags (like [happy]) will override these sliders for that specific line only.
    communicate = edge_tts.Communicate(final_text, v_code, rate=rate, pitch=pitch)
    
    output_file = "rajdev_voice.mp3"
    await communicate.save(output_file)
    return output_file

if st.button("Generate Audio 🎧", type="primary"):
    if not text_input:
        st.warning("Script khali hai!")
    else:
        status = st.empty()
        status.text("Generating...")
        
        try:
            output_path = asyncio.run(generate_audio(text_input, selected_voice_code, rate_str, pitch_str))
            
            status.text("✅ Done!")
            st.audio(output_path, format='audio/mp3')
            
            st.success(f"Voice: {selected_voice_name} | Speed: {rate_str} | Pitch: {pitch_str}")
            
        except Exception as e:
            st.error(f"Error: {e}")
            
