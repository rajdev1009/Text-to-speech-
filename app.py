import streamlit as st
import edge_tts
import asyncio
import os

# --- Page Config ---
st.set_page_config(page_title="Raj Audio Studio", page_icon="🎙️")
st.title("✅ AstraToonix Final Studio")

# --- UPDATED CAPTION ---
# Aapke kahe mutabik line change kar di hai:
st.caption("Welcome Raj Audio Studio | Feedback Dena mat bhulna")

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

# --- 3. Script Input (UPDATED) ---
st.markdown("### Script:")

# Aapki Biodata Script yahan default set kar di hai
default_text = """नमस्ते दोस्तों! मेरा नाम है राजदेव।

दुनिया को लगता है कि मैं सिर्फ एक कंप्यूटर के सामने बैठने वाला, चश्मा लगाने वाला बोरिंग डेवलपर हूँ। कोड लिखना, बग्स फिक्स करना और काली स्क्रीन पर हरी लाइनें देखना... यह मेरा पेशा है। मैं एक डेवलपर हूँ।

लेकिन रुकिए! कहानी यहाँ खत्म नहीं होती! इस कोडिंग वाली सीरियस ज़िंदगी के पीछे, एक ऐसा इंसान भी है जिसे लोगों को हँसाना पसंद है।

जब कीबोर्ड की खट-खट से मेरा दिमाग थक जाता है, तब शुरू होता है मेरा असली मैजिक! मैं क्रिएटर हूँ AstraToonix का!

हाँ, वही चैनल जहाँ लॉजिक की ऐसी-तैसी करके हम सिर्फ मजे की बात करते हैं। कोडिंग मेरा दिमाग है, लेकिन AstraToonix मेरा दिल है।

तो अगर आप टेक्नोलॉजी और मस्ती, दोनों का मज़ा एक साथ लेना चाहते हैं... तो स्वागत है मेरी दुनिया में! मैं हूँ राजदेव, और अभी तो बस शुरुआत है!"""

# Height badha di hai taaki script puri dikhe
text_input = st.text_area("Yahan likhein:", default_text, height=350)

# --- 4. Logic (No Coding Errors) ---
async def generate_audio(text, v_code, rate, pitch):
    # Newline fix for better flow
    clean_text = text.replace("\n", " ")
    
    # Direct Communicate (No SSML code injection)
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
            
