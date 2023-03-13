import io

import numpy as np
import pretty_midi
import requests
import streamlit as st
from scipy.io import wavfile

st.markdown(f"<h1 style='text-align: center;'> 🤖 Music Generator 🤖 </h1>", unsafe_allow_html=True)
style = st.sidebar.selectbox(
        "🎹 Select your style 🎸",
        ("Daft Punk", "J.S. Bach", "Britney Spears"))
temperature = st.sidebar.slider('🌶️ Spice levels 🌶️', 0.1, 1.0, 0.01)
bars = st.sidebar.select_slider('How many bars?', options=[4, 8, 16])

url = ''
params = {
"style": style,
"temperature":temperature,
"bars":bars}


response = requests.get(url, params)
# fare = round(response.json()['fare'])

st.markdown(f'# Nothing to show here yet :)')
st.set_page_config(
        page_title="MIDI to WAV",
        page_icon="musical_note",
        initial_sidebar_state="collapsed")
