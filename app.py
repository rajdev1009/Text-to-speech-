import streamlit as st
import edge_tts
import asyncio
import os

# --- Page Config ---
st.set_page_config(page_title="AstraToonix Studio", page_icon="🎚️")
st.title("🎚️ AstraToonix Pro Studio (Fixed)")
st.caption("No More Reading Tags Error 🚫")

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
st.markdown("### Script Editor:")
default_text = """अरे भाई क्या हाल है? [laugh]
आज तो मजा ही आ गया यार! [happy]
तुम वहाँ क्यों खड़े हो? [angry] जल्दी इधर आओ!"""

text_input = st.text_area("Yahan likhein:", default_text, height=150)

st.markdown("""
**Tags:** `[laugh]`, `[happy]`, `[angry]`
""")

# --- 4. The Logic Fix (SSML Wrapper) ---
def build_ssml(text, voice, global_rate, global_pitch):
    # A. Text Cleaning
    text = text.replace("\n", " ")
    
    # B. Replace Tags with SSML codes
    # Laughter
    text = text.replace("[laugh]", '<prosody rate="+50%" pitch="+15Hz">हहाहाहाहाहा</prosody>')
    
    # Happy
    text = text.replace("[happy]", '<prosody rate="+20%" pitch="+10Hz">')
    
    # Angry
    text = text.replace("[angry]", '<prosody rate="+0%" pitch="-10Hz">')
    
    # Close Tags Logic
    # (Jugaad: Jahan bhi naya tag shuru ho, wahan pichla band maana jaye, 
    # lekin simple rakhne ke liye hum user se expect karte hain wo sentence khatam kare)
    if "[happy]" in text or "[angry]" in text:
        text = text + "</prosody>"
        
    # C. WRAP EVERYTHING IN FULL SSML STRUCTURE (Ye zaruri hai!)
    # Hum Global Speed aur Pitch yahan laga rahe hain taaki 'edge-tts' confuse na ho.
    ssml_content = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='hi-IN'>
        <voice name='{voice}'>
            <prosody rate='{global_rate}' pitch='{global_pitch}'>
                {text}
            </prosody>
        </voice>
    </speak>
    """
    return ssml_content

# --- 5. Generation ---
async def generate_audio(text, v_code, rate, pitch):
    # Step 1: Pura SSML khud banao
    final_ssml = build_ssml(text, v_code, rate, pitch)
    
    # Step 2: Communicate ko bhejo (Lekin rate/pitch argument mat do, kyunki wo SSML me hai)
    communicate = edge_tts.Communicate(final_ssml, v_code)
    
    output_file = "rajdev_fixed.mp3"
    await communicate.save(output_file)
    return output_file

if st.button("Generate Audio 🎧", type="primary"):
    if not text_input:
        st.warning("Script khali hai!")
    else:
        status = st.empty()
        status.text("Fixing Tags & Generating...")
        
        try:
            output_path = asyncio.run(generate_audio(text_input, selected_voice_code, rate_str, pitch_str))
            
            status.text("✅ Done!")
            st.audio(output_path, format='audio/mp3')
            st.success("Ab ye tags ko bolega nahi, apply karega!")
            
        except Exception as e:
            st.error(f"Error: {e}")
            
