import streamlit as st
import edge_tts
import asyncio
import os

# --- Page Config ---
st.set_page_config(page_title="AstraToonix Studio", page_icon="🎙️")

# --- 1. TITLE & DISCLAIMER (Updated) ---
st.title("AstraToonix")  # Main Title
st.caption("Welcome to Raj Audio Studio | Feedback Dena mat bhulna")

# Disclaimer Box
st.warning("""
⚠️ **जरूरी सूचना (Disclaimer):**
* अगर आपने **Hindi Voice** चुनी है, तो बॉक्स में **हिंदी शब्द (Hindi Words)** ही लिखें।
* अगर आप **English Voice** use कर रहे हैं, तो **Full English** में ही लिखें।
* मिक्स करने पर (खिचड़ी भाषा में) आवाज़ सही नहीं आएगी।
""")

# --- 2. EXPANDED VOICE LIST (12 Voices) ---
voice_options = {
    # --- Hindi Voices ---
    "🇮🇳 Hindi - Rajdev (Male)": "hi-IN-MadhurNeural",
    "🇮🇳 Hindi - Swara (Female)": "hi-IN-SwaraNeural",
    
    # --- Indian English ---
    "🇮🇳 English (India) - Prabhat (Male)": "en-IN-PrabhatNeural",
    "🇮🇳 English (India) - Neerja (Female)": "en-IN-NeerjaNeural",
    
    # --- US English ---
    "🇺🇸 English (US) - Christopher (Movie Guy)": "en-US-ChristopherNeural",
    "🇺🇸 English (US) - Guy (Standard Male)": "en-US-GuyNeural",
    "🇺🇸 English (US) - Jenny (Standard Female)": "en-US-JennyNeural",
    "🇺🇸 English (US) - Aria (Energetic)": "en-US-AriaNeural",
    "🇺🇸 English (US) - Ana (Child Voice)": "en-US-AnaNeural",
    
    # --- UK English ---
    "🇬🇧 English (UK) - Ryan (Male)": "en-GB-RyanNeural",
    "🇬🇧 English (UK) - Sonia (Female)": "en-GB-SoniaNeural",
    
    # --- Heavy ---
    "🇺🇸 English (US) - Eric (Heavy Male)": "en-US-EricNeural"
}

selected_voice_name = st.selectbox("Select Voice (Character):", list(voice_options.keys()))
selected_voice_code = voice_options[selected_voice_name]

# --- 3. Sliders ---
col1, col2 = st.columns(2)
with col1:
    rate_val = st.slider("Speed (Flow)", -50, 50, 10, format="%d%%")
    rate_str = f"{rate_val:+d}%"

with col2:
    pitch_val = st.slider("Pitch (Tone)", -20, 20, -2, format="%dHz")
    pitch_str = f"{pitch_val:+d}Hz"

# --- 4. Script Input ---
st.markdown("### Script:")

default_text = """नमस्ते दोस्तों! मेरा नाम है राजदेव।

दुनिया को लगता है कि मैं सिर्फ एक कंप्यूटर के सामने बैठने वाला, चश्मा लगाने वाला बोरिंग Developer हूँ। कोड लिखना, बग्स फिक्स करना और काली स्क्रीन पर हरी लाइनें देखना... यह मेरा पेशा है। मैं एक Developer हूँ।

लेकिन रुकिए! कहानी यहाँ खत्म नहीं होती! इस कोडिंग वाली सीरियस ज़िंदगी के पीछे, एक ऐसा इंसान भी है जिसे लोगों को हँसाना पसंद है।

जब कीबोर्ड की खट-खट से मेरा दिमाग थक जाता है, तब शुरू होता है मेरा असली मैजिक! मैं क्रिएटर हूँ AstraToonix का!

हाँ, वही चैनल जहाँ लॉजिक की ऐसी-तैसी करके हम सिर्फ मजे की बात करते हैं। कोडिंग मेरा दिमाग है, लेकिन AstraToonix मेरा दिल है।

तो अगर आप टेक्नोलॉजी और मस्ती, दोनों का मज़ा एक साथ लेना चाहते हैं... तो स्वागत है मेरी दुनिया में! मैं हूँ राजदेव, और अभी तो बस शुरुआत है!"""

text_input = st.text_area("Yahan likhein:", default_text, height=350)

# --- 5. Logic ---
async def generate_audio(text, v_code, rate, pitch):
    clean_text = text.replace("\n", " ")
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
            output_path = asyncio.run(generate_audio(text_input, selected_voice_code, rate_str, pitch_str))
            
            status.text("✅ Done!")
            st.audio(output_path, format='audio/mp3')
            st.success(f"Character: {selected_voice_name}")
            
            # --- Download Button ---
            with open(output_path, "rb") as file:
                st.download_button(
                    label="Download MP3 📥",
                    data=file,
                    file_name="AstraToonix_Audio.mp3",
                    mime="audio/mpeg"
                )
            
        except Exception as e:
            st.error(f"Error: {e}")
            
