import streamlit as st
from TTS.api import TTS
import sounddevice as sd
import scipy.io.wavfile as wav
import os
import time


# -------- XTTS SAFE ADVANCED EMOTION ENGINE ----------
EMOTION_STYLES = {
    "friendly": {"speed": 1.0},
    "angry": {"speed": 1.3},
    "storytelling": {"speed": 0.85},
    "calm": {"speed": 0.75},
    "robot": {"speed": 1.05}
}



# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="Chatterbox AI Voice Cloner", layout="wide")

if not os.path.exists("voices"):
    os.makedirs("voices")
if not os.path.exists("output"):
    os.makedirs("output")

# ---------------- LOAD MODEL ---------------- #
@st.cache_resource
def load_model():
    return TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True)


tts = load_model()

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🎚 Chatterbox Controls")
st.sidebar.markdown("### ✅ Voice Cloning System")
st.sidebar.info("Upload clean 5–10 sec WAV voice")

voice_sample = st.sidebar.file_uploader("Upload Reference Voice", type=["wav"])

if voice_sample:
    with open("voices/reference.wav", "wb") as f:
        f.write(voice_sample.read())
    st.sidebar.audio("voices/reference.wav")

# ---------------- MAIN UI ---------------- #
st.title("🎧 Chatterbox AI Voice Cloning Studio")
st.caption("Real-time Text-to-Speech & Speech-to-Speech Voice Cloning")

tab1, tab2 = st.tabs(["📝 Text → Voice", "🎤 Speech → Voice"])

# ============= TAB 1 : TEXT TO VOICE ============= #
with tab1:
    st.header("Text → Voice")

    text_input = st.text_area("Enter text to speak", height=200)

    # ✅ ✅ ✅ PASTE HERE (ADVANCED EMOTION UI STARTS HERE)
    st.subheader("🎭 Advanced Emotion Controls")

    emotion = st.selectbox(
       "Select Voice Emotion",
       list(EMOTION_STYLES.keys())
   )

    emotion_strength = st.slider(
        "Emotion Strength",
        0.5, 2.0, 1.0
   )

    speed = st.slider(
        "Speech Speed",
        0.5, 1.6,
    EMOTION_STYLES[emotion]["speed"]
)

    # ✅ ✅ ✅ PASTE ENDS HERE

    if st.button("🎙 Speak Text"):
        # your TTS code here

        if not voice_sample:
            st.error("❌ Please upload a reference voice!")
        elif text_input.strip() == "":
            st.error("❌ Please enter some text!")
        else:
            with st.spinner("Cloning Voice... Please wait"):
                output_path = "output/cloned_voice.wav"
                tts.tts_to_file(
                    text=text_input,
                    speaker_wav="voices/reference.wav",
                    file_path=output_path,
                    language="en",
                    speed=speed * emotion_strength
          )


                time.sleep(1)

            st.success("✅ Voice Generated Successfully!")
            st.audio(output_path)
            st.download_button("⬇ Download Audio", open(output_path, "rb"), file_name="cloned_voice.wav")

# ============= TAB 2 : SPEECH TO VOICE ============= #
with tab2:
    st.subheader("Record Voice & Convert to Cloned Voice")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎤 Start Recording"):
            fs = 16000
            duration = 5
            st.info("Recording for 5 seconds...")
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()
            wav.write("output/input_speech.wav", fs, recording)
            st.success("✅ Recording Completed")
            st.audio("output/input_speech.wav")

    with col2:
        if st.button("🔁 Convert to Cloned Voice"):
            if not os.path.exists("output/input_speech.wav"):
                st.error("❌ Please record voice first!")
            elif not voice_sample:
                st.error("❌ Upload reference voice first!")
            else:
                with st.spinner("Cloning Your Voice..."):
                    output_path = "output/speech_clone.wav"
                    tts.tts_to_file(
                       text=text_input,
                       speaker_wav="voices/reference.wav",
                       file_path=output_path,
                       language="en",
                       speed=speed * emotion_strength
 )
                   

                    
                time.sleep(1)

                st.success("✅ Speech Converted Successfully!")
                st.audio(output_path)
                st.download_button("⬇ Download Audio", open(output_path, "rb"), file_name="speech_clone.wav")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.markdown("✅ Built with **Python + Streamlit + Chatterbox TTS AI**")
st.markdown("🚀 Professional AI Voice Cloning System")


# -------- ADVANCED EMOTION ENGINE ----------

