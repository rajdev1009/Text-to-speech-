import streamlit as st
import edge_tts
import asyncio
import os

# --- Page Config ---
st.set_page_config(page_title="AstraToonix Pro Studio", page_icon="🎭")

st.title("🎭 AstraToonix Pro Voice Studio")
st.info("💡 Tip: Use tags like [pause], [fast], [laugh] to make it realistic!")

# --- Voice Settings ---
voice_options = {
    "Hindi - Madhur (Male)": "hi-IN-MadhurNeural",
    "Hindi - Swara (Female)": "hi-IN-SwaraNeural",
    "English - Christopher": "en-US-ChristopherNeural"
}
selected_voice = st.selectbox("Select Voice:", list(voice_options.keys()))
voice_code = voice_options[selected_voice]

# --- Input Area ---
default_text = """नमस्ते दोस्तों! [pause] 
आज हम कुछ तूफानी करने वाले हैं। [laugh]
क्या आप तैयार हैं? [fast] जल्दी बताओ भाई देर हो रही है! [normal]
आराम से रिलैक्स होकर बैठो।"""

text_input = st.text_area("Script Editor:", default_text, height=200)

# --- Helper Buttons for Tags ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.caption("**[pause]** = 1 sec break")
with col2:
    st.caption("**[laugh]** = Fake laugh")
with col3:
    st.caption("**[fast]** = Excited speed")
with col4:
    st.caption("**[slow]** = Sad/Serious")

# --- SSML Processor (The Magic Logic) ---
def process_text_to_ssml(text, voice):
    # 1. Newlines remove karein taaki flow na tute (Flow fix)
    clean_text = text.replace("\n", " ")
    
    # 2. Convert custom tags to Microsoft SSML
    # Break/Pause
    clean_text = clean_text.replace("[pause]", '<break time="800ms"/>')
    clean_text = clean_text.replace("[long_pause]", '<break time="1500ms"/>')
    
    # Laughter (Jugaad: High pitch + Fast speed)
    laugh_ssml = '<prosody rate="+50%" pitch="+15Hz">हा हा हा हा</prosody>'
    clean_text = clean_text.replace("[laugh]", laugh_ssml)
    
    # Fast / Excited
    clean_text = clean_text.replace("[fast]", '<prosody rate="+20%" pitch="+5Hz">')
    
    # Slow / Serious
    clean_text = clean_text.replace("[slow]", '<prosody rate="-10%" pitch="-5Hz">')
    
    # Reset to Normal (Closing the tag)
    clean_text = clean_text.replace("[normal]", '</prosody>')
    
    # 3. Wrap in full SSML structure
    ssml_content = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='hi-IN'>
        <voice name='{voice}'>
            {clean_text}
        </voice>
    </speak>
    """
    return ssml_content

# --- Generation Logic ---
async def generate_audio(ssml_data):
    communicate = edge_tts.Communicate(ssml_data, voice_code)
    output_file = "output_pro.mp3"
    # SSML mode on karne ke liye text ko directly nahi, ssml=True bhejna padta hai,
    # lekin edge-tts library me direct ssml string pass karte hain communicate me.
    await communicate.save(output_file)
    return output_file

if st.button("Generate Realistic Audio 🎬", type="primary"):
    if not text_input:
        st.warning("Kuch likhiye to sahi!")
    else:
        status = st.empty()
        status.text("Processing Emotion Tags...")
        
        try:
            # Step 1: Text ko SSML codes me badlo
            final_ssml = process_text_to_ssml(text_input, voice_code)
            
            # Step 2: Audio banao
            output_path = asyncio.run(generate_audio(final_ssml))
            
            status.text("✅ Done!")
            st.audio(output_path, format='audio/mp3')
            st.success("Audio Generated with Emotions!")
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.warning("Agar error aaye, to check karein ki [fast] tag ke baad [normal] lagaya hai ya nahi.")

st.markdown("---")
st.caption("AstraToonix Pro | Powered by Edge SSML")
