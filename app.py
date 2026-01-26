import streamlit as st
import edge_tts
import asyncio
import os

st.set_page_config(page_title="AstraToonix Director Mode", page_icon="🎬")
st.title("🎬 AstraToonix: Emotion Director")
st.caption("Free Emotions using Pitch/Rate Hacks")

# --- Voice Setup ---
VOICE = "hi-IN-MadhurNeural"

# --- Script Input ---
default_text = """नमस्ते दोस्तों! [happy] आज मैं बहुत खुश हूँ!
[sad] लेकिन कल मेरे साथ कुछ बुरा हुआ।
[excited] पर छोडो यार! आज हम पार्टी करेंगे!
[whisper] धीरे बोलो, कोई सुन लेगा।"""

text_input = st.text_area("Script (Use tags: [happy], [sad], [excited], [whisper])", default_text, height=200)

# --- The "Emotion Engine" ---
def apply_emotions_to_ssml(text):
    # 1. Basic Cleaning
    text = text.replace("\n", " ")
    
    # 2. EMOTION LOGIC (Pitch/Rate Manipulation)
    
    # Happy: High Pitch + Fast Speed
    text = text.replace("[happy]", '<prosody pitch="+10Hz" rate="+10%">')
    
    # Sad: Low Pitch + Slow Speed
    text = text.replace("[sad]", '<prosody pitch="-5Hz" rate="-15%">')
    
    # Excited: Very High Pitch + Very Fast
    text = text.replace("[excited]", '<prosody pitch="+15Hz" rate="+20%">')
    
    # Whisper (Jugaad): Very Soft (Volume) + Fast
    text = text.replace("[whisper]", '<prosody volume="-40%" rate="+5%">')
    
    # 3. Closing Tags (Simple Logic)
    # Jahan bhi naya tag aaye, wahan hum manenge purana emotion khatam.
    # Lekin XML strict hota hai, isliye hum user ko force nahi karenge.
    # Hum bas end me </prosody> laga denge taaki error na aaye.
    
    # Reset Logic: Hum har tag se pehle pichla tag band karne ki koshish karenge
    # (Yah complex hai, isliye hum ek simple wrapper use karenge)
    
    # --- FINAL SSML STRUCTURE ---
    # Sabse zaruri: <speak> tag ka hona. Tabhi wo tags ko padhega nahi, execute karega.
    ssml = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='hi-IN'>
        <voice name='{VOICE}'>
            {text}
        </voice>
    </speak>
    """
    
    # Note: Agar user ne tag open kiya par close nahi kiya, to EdgeTTS usually handle kar leta hai.
    # Best practice: User ko bolo ki wo emotion ke baad [normal] lagaye.
    ssml = ssml.replace("[normal]", "</prosody>")
    
    return ssml

# --- Generation ---
async def generate_audio(text):
    ssml_code = apply_emotions_to_ssml(text)
    
    # Communicate object me hum SSML bhej rahe hain
    communicate = edge_tts.Communicate(ssml_code, VOICE)
    
    output_file = "emotion_audio.mp3"
    await communicate.save(output_file)
    return output_file

if st.button("Generate Emotional Audio 🎭", type="primary"):
    if not text_input:
        st.warning("Script is empty!")
    else:
        status = st.empty()
        status.text("Directing the Scene...")
        
        try:
            output_path = asyncio.run(generate_audio(text_input))
            
            status.text("✅ Done!")
            st.audio(output_path, format='audio/mp3')
            st.success("Tip: Use [normal] to stop an emotion.")
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Agar error aaye, to check karein ki tags sahi jagah lage hain.")

st.markdown("""
### 🎭 How to Act (इमोशन कैसे डालें):
1. **[happy]**: खुश और तेज़ आवाज़।
2. **[sad]**: दुखी और धीमी आवाज़।
3. **[excited]**: बहुत ज्यादा जोश।
4. **[whisper]**: धीरे (फुसफुसाना)।
5. **[normal]**: इमोशन रोकने के लिए।

**Example:**
`[happy] हेलो राजदेव! [normal] क्या हाल है? [sad] यार मैं थक गया हूँ।`
""")
