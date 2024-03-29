import os
import json
import magenta
import magenta.music as mm
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from magenta.models.music_vae import configs
from magenta.models.music_vae.trained_model import TrainedModel
from magenta.music import concatenate_sequences
from starlette.responses import Response
from magenta.music.midi_io import note_sequence_to_pretty_midi
import pretty_midi
import mido



app = FastAPI()

list_sf2 = {"italo_disco": "gs://wagon_human_bucket/sf2/Super_Italo_DiscoFont_Director_s_Cut.sf2",
            "japan_pop": "gs://wagon_human_bucket/sf2/Japan_Herentals.sf2",
            "piano_guitar_bass": "gs://wagon_human_bucket/sf2/SGM-v2.01-NicePianosGuitarsBass-V1.2.sf2",
            "marimba": "gs://wagon_human_bucket/sf2/Versilian_Studios_Marimba.sf2",
            "techno": "gs://wagon_human_bucket/sf2/20_synths.sf2",
            "mario_kart":  "gs://wagon_human_bucket/sf2/Mario_Kart_Collection.sf2",
            "latin_music":  "gs://wagon_human_bucket/sf2/Escudero_Piano_M1.sf2"}


BATCH_SIZE = 32
Z_SIZE = 512
TOTAL_STEPS = 2048
BAR_SECONDS = 1.5
CHORD_DEPTH = 49

SAMPLE_RATE = 44500

# Get model from bucket


#Load model
config = configs.CONFIG_MAP['hierdec-trio_16bar']

#hierdec-trio_16bar
model = TrainedModel(config, batch_size=BATCH_SIZE, checkpoint_dir_or_path = "gs://download.magenta.tensorflow.org/models/music_vae/colab2" + '/checkpoints/trio_16bar_hierdec.ckpt')

model._config.data_converter._max_tensors_per_input = None

# Convertir un fichier MIDI en JSON
def midi_to_json(midi_file):
    midi_data = mido.MidiFile(midi_file)
    json_data = [message.dict() for message in midi_data]
    return json.dumps(json_data)

# Spherical linear interpolation.
def slerp(p0, p1, t):
  """Spherical linear interpolation."""
  omega = np.arccos(np.dot(np.squeeze(p0/np.linalg.norm(p0)), np.squeeze(p1/np.linalg.norm(p1))))
  so = np.sin(omega)
  return np.sin((1.0-t)*omega) / so * p0 + np.sin(t*omega)/so * p1


# Chord encoding tensor.
def chord_encoding(chord):
  index = mm.TriadChordOneHotEncoding().encode_event(chord)
  c = np.zeros([TOTAL_STEPS, CHORD_DEPTH])
  c[0,0] = 1.0
  c[1:,index] = 1.0
  return c

# Trim sequences to exactly one bar.
def trim_sequences(seqs, num_seconds=BAR_SECONDS):
  for i in range(len(seqs)):
    seqs[i] = mm.extract_subsequence(seqs[i], 0.0, num_seconds)
    seqs[i].total_time = num_seconds

# Consolidate instrument numbers by MIDI program.
def fix_instruments_for_concatenation(note_sequences):
  instruments = {}
  for i in range(len(note_sequences)):
    for note in note_sequences[i].notes:
      if not note.is_drum:
        if note.program not in instruments:
          if len(instruments) >= 8:
            instruments[note.program] = len(instruments) + 2
          else:
            instruments[note.program] = len(instruments) + 1
        note.instrument = instruments[note.program]
      else:
        note.instrument = 9

@app.get("/generate_music") #URL schema http://localhost:8080/generate_music?style=italo_disco&num_bars=20&temperature=1
async def generate_music(style: str, num_bars: int = 48, temperature: float = 1):
    z1 = np.random.normal(size=[Z_SIZE])
    z2 = np.random.normal(size=[Z_SIZE])
    z = np.array([slerp(z1, z2, t)
                for t in np.linspace(0, 1, num_bars)])

    seqs = model.decode(length=TOTAL_STEPS, z=z, temperature=temperature)

    trim_sequences(seqs)
    fix_instruments_for_concatenation(seqs)
    interp_ns = concatenate_sequences(seqs)

    #Conversion start, to send through API
    test = note_sequence_to_pretty_midi(interp_ns)
    tracks_dict = {}
    for i, track in enumerate(test.instruments):
        tracks_dict[f"track_{i+1}"] = {
            "program": track.program,
            "is_drum": track.is_drum,
            "notes": [{"pitch": note.pitch, "start": note.start, "end": note.end, "velocity": note.velocity}
                    for note in track.notes]
        }
    return tracks_dict

@app.get("/")
async def root():
    result = {
        'dumb': 'Hello'
    }
    return result
