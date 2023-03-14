import io

import numpy as np
import pretty_midi
import requests
import streamlit as st
from scipy.io import wavfile

st.set_page_config(
        page_title="MIDI to WAV",
        page_icon="musical_note",
        initial_sidebar_state="expanded")
st.markdown(f"<h1 style='text-align: center;'> 🤖 Music Generator 🤖 </h1>", unsafe_allow_html=True)
style = st.sidebar.selectbox(
        "🎹 Select your style 🎸",
        ("🤌 Italo Disco", 
         "🇯🇵 Japan pop",
         "🎻 Piano Guitar Bass",
         "🌊 Marimba",
         "🔌💻 Techno",
         "🏎️ Mario Kart",
         "💃 Latin Music"))
temperature = st.sidebar.slider('🌶️ Spice levels 🌶️', 0.01, 1.5, 0.01)
bars = st.sidebar.select_slider('How many bars?', options=[4, 8, 16])

style2 = "_".join(style.lower())
temperature2 = temperature * 10 
url = 'https://zikosv1-22biky57hq-ew.a.run.app/generate_music'
params = {
"style": style,
"nb_bars":bars,
"temperature":temperature
}
with st.spinner(f"Fetching Request"):
        response = requests.get(url, params).json()
with st.spinner(f"Transcribing to FluidSynth"):
        midi_data = pretty_midi.PrettyMIDI(response)
        audio_data = midi_data.fluidsynth()
        audio_data = np.int16(
            audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
        )
        virtualfile = io.BytesIO()
        wavfile.write(virtualfile, 44100, audio_data)
st.audio(virtualfile)
