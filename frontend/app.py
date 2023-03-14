
import io
import json

import mido
import numpy as np
import pretty_midi
import pygame
import requests
import streamlit as st
from IPython.display import Audio, display
from scipy.io import wavfile

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

url = 'https://human-22biky57hq-ew.a.run.app/generate_music'
params = {
"style": style,
"nb_bars":bars,
"temperature":temperature
}

#loop pour récupérer un fichier pretty-midi depuis un dict


def json_to_midi(json_data):
    midi_data = pretty_midi.PrettyMIDI()
    for track_name, track_info in json_data.items():
        # créer une instance de pretty_midi.Instrument()
        instr = pretty_midi.Instrument(program=track_info['program'], is_drum=track_info['is_drum'])
        # ajouter les notes à l'instrument
        for note_info in track_info['notes']:
            note = pretty_midi.Note(
                velocity=note_info['velocity'],
                pitch=note_info['pitch'],
                start=note_info['start'],
                end=note_info['end']
            )
            instr.notes.append(note)
            # ajouter l'instrument au fichier midi
        midi_data.instruments.append(instr)
    return midi_data

# def json_to_midi(json_data):
#     # Create MIDI file
#     midi_data = mido.MidiFile(type=0)

#     # Add tracks to MIDI file
#     for track_data in json_data['tracks']:
#         track = mido.MidiTrack()
#         midi_data.tracks.append(track)

#         # Add messages to track
#         for msg_data in track_data['messages']:
#             msg = mido.Message.from_dict(msg_data)
#             track.append(msg)

#     return midi_data

with st.spinner(f"Fetching Request"):
        response = requests.get(url, params).json()

st.write(response)

with st.spinner(f"Turning JSON to MIDI..."):
        midi_data = json_to_midi(response)
        midi_data.write('output.mid')

# with st.spinner(f"Loading MIDI player"):
#         pygame.mixer.init()

# audio_data=midi_data.synthesize()
# display(Audio(audio_data, rate=44000))

with st.spinner(f"Transcribing to FluidSynth"):
    audio_data = midi_data.fluidsynth()
    audio_data = np.int16(
        audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
    )  # -- Normalize for 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

    virtualfile = io.BytesIO()
    wavfile.write(virtualfile, 44100, audio_data)

st.audio(virtualfile)
