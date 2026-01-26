import streamlit as st
import edge_tts
import asyncio
import os

# --- Page Config ---
st.set_page_config(page_title="AstraToonix Clean Studio", page_icon="🎙️")
st.title("🎙️ AstraToonix Studio (Clean Audio)")
st.caption("No Robotic Commands in Audio 🚫 | Pure Script Only")

# --- 1. Voice Setup ---
voice_options = {
    "Hindi - Rajdev (Male)": "hi-IN-MadhurNeural",
    "Hindi - Swara (Female)": "hi-IN-SwaraNeural",
    "English - Christopher": "en-US-ChristopherNeural"
}

selected_voice_name = st.selectbox("Select Voice:", list(voice_options.keys()))
selected_voice_code = voice_options[selected_voice_name]

# --- 2. Sliders ---
col1, col2 = st.columns(2)
with col1:
    rate_val = st.slider("Global Speed", -50, 50, 10, format="%d%%")
    rate_str = f"{rate_val:+d}%"
with col2:
    pitch_val = st.slider("Global Pitch", -20, 20, -2, format="%dHz")
    pitch_str = f"{pitch_val:+d}Hz"

# --- 3. Script Input ---
default_text = """अरे भाई क्या हाल है? [laugh]
आज तो मजा ही आ गया यार! [happy]
तुम वहाँ क्यों खड़े हो? [angry] जल्दी इधर आओ!"""

text_input = st.text_area("Script Editor:", default_text, height=150)

st.info("Tags Supported: `[laugh]`, `[happy]`, `[angry]`")

# --- 4. Logic Fix (No More Metadata Reading) ---
def clean_ssml(text, global_rate, global_pitch):
    # A. Text Cleaning
    text = text.replace("\n", " ")
    
    # B. Replace Tags with simple Prosody changes
    # Laughter
    text = text.replace("[laugh]", '<prosody rate="+50%" pitch="+15Hz">हहाहाहाहाहा</prosody>')
    
    # Happy
    text = text.replace("[happy]", '<prosody rate="+20%" pitch="+10Hz">')
    
    # Angry
    text = text.replace("[angry]", '<prosody rate="+0%" pitch="-10Hz">')
    
    # Close Tags Logic
    if "[happy]" in text or "[angry]" in text:
        text = text + "</prosody>"
        
    # C. FINAL SSML STRUCTURE (Simple Wrapper)
    # Note: Maine yahan se <voice> tag hata diya hai. 
    # Ab ye sirf <speak> aur <prosody> use karega.
    # .strip() lagaya hai taaki extra space ki wajah se wo code ko text na samjhe.
    
    ssml_content = f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='hi-IN'><prosody rate='{global_rate}' pitch='{global_pitch}'>{text}</prosody></speak>"""
    
    return ssml_content.strip()

# --- 5. Generation ---
async def generate_audio(text, v_code, rate, pitch):
    # Step 1: Clean SSML banao
    final_ssml = clean_ssml(text, rate, pitch)
    
    # Step 2: Communicate (Is baar hum rate/pitch alag se nahi bhejenge, wo SSML me hai)
    communicate = edge_tts.Communicate(final_ssml, v_code)
    
    output_file = "rajdev_clean.mp3"
    await communicate.save(output_file)
    return output_file

if st.button("Generate Clean Audio 🎧", type="primary"):
    if not text_input:
        st.warning("Script khali hai!")
    else:
        status = st.empty()
        status.text("Generating...")
        
        try:
            output_path = asyncio.run(generate_audio(text_input, selected_voice_code, rate_str, pitch_str))
            
            status.text("✅ Done!")
            st.audio(output_path, format='audio/mp3')
            
        except Exception as e:
            st.error(f"Error: {e}")
            
