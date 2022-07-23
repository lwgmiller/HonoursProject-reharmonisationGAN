import numpy as np


# Data
n_tracks = 4  # number of tracks
n_pitches = 83  # number of pitches
lowest_pitch = 24  # MIDI note number of the lowest pitch
n_samples_per_song = 8  # number of samples to extract from each song in the datset
n_measures = 2  # number of measures per sample
beat_resolution = 4  # temporal resolution of a beat (in timestep)
programs = [0, 0, 0, 0]  # program number for each track
is_drums = [False, False, False, False]  # drum indicator for each track
track_names = ['Soprano', 'Alto', 'Tenor', 'Bass']  # name of each track
tempo = 100

measure_resolution = 4 * beat_resolution
tempo_array = np.full((4 * 4 * measure_resolution, 1), tempo)

# Training
batch_size = 16
latent_dim = 128
n_steps = 1000

# Sampling
sample_interval = 10  # interval to run the sampler (in step)
n_samples = 4
