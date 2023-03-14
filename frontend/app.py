
import numpy as np
import requests
import streamlit as st
import pygame
import json
import mido

st.set_page_config(
        page_title="🔥",
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

url = 'https://human-22biky57hq-ew.a.run.app'
params = {
"style": style,
"nb_bars":bars,
"temperature":temperature
}


def json_to_midi(json_data):
    # Create MIDI file
    midi_data = mido.MidiFile(type=0)

    # Add tracks to MIDI file
    for track_data in json_data['tracks']:
        track = mido.MidiTrack()
        midi_data.tracks.append(track)

        # Add messages to track
        for msg_data in track_data['messages']:
            msg = mido.Message.from_dict(msg_data)
            track.append(msg)

    return midi_data

with st.spinner(f"Fetching Request"):
        response = requests.get(url, params).json()

with st.spinner(f"Turning JSON to MIDI..."):
        midi_data = json_to_midi(response)

with st.spinner(f"Loading MIDI player"):
        pygame.mixer.init()

if st.button('Play MIDI'):
    pygame.mixer.music.load(midi_data)
    pygame.mixer.music.play()
