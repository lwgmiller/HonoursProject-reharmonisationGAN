import pypianoroll
import numpy as np


from tqdm import tqdm


import settings

def Get_V_Samples(data: list):

  dataS = []
  for multitrack in tqdm(data):
    
    multitrack.binarize()
      # Downsample the pianorolls (shape: n_timesteps x n_pitches)
    multitrack.set_resolution(settings.beat_resolution)
      # Stack the pianoroll (shape: n_tracks x n_timesteps x n_pitches)
    pianoroll = (multitrack.stack() > 0)
    
      # Get the target pitch range only
    pianoroll = pianoroll[:, :, settings.lowest_pitch:settings.lowest_pitch + (settings.n_pitches + 1)] 
    #print(pianoroll.shape) 
      # Calculate the total measures
    n_total_measures = multitrack.get_max_length() // settings.measure_resolution
    candidate = n_total_measures - settings.n_measures
    target_n_samples = min(n_total_measures // settings.n_measures, settings.n_samples_per_song)
    stepsPerSample = settings.n_measures * settings.measure_resolution
      # Randomly select a number of phrases from the multitrack pianoroll
    for i in range(0, multitrack.get_max_length(), stepsPerSample):

      if (pianoroll.sum(axis=(1, 2)) < 10).any():
          continue
    
      dataS.append(pianoroll[:, i:i + stepsPerSample])
  # Stack all the collected pianoroll segments into one big array
  #random.shuffle(dataS)
  dataS = np.stack(dataS)
  print(f"Successfully collect {len(dataS)} samples from {len(data)} songs")
  print(f"Data shape : {dataS.shape}")
  print(dataS.shape)

  return dataS

def Get_Samples(data: list):

  dataS = []
  for multitrack in tqdm(data):
    
    multitrack.binarize()
      # Downsample the pianorolls (shape: n_timesteps x n_pitches)
    multitrack.set_resolution(settings.beat_resolution)
      # Stack the pianoroll (shape: n_tracks x n_timesteps x n_pitches)
    pianoroll = (multitrack.stack() > 0)
    
      # Get the target pitch range only
    pianoroll = pianoroll[:, :, settings.lowest_pitch:settings.lowest_pitch + (settings.n_pitches + 1)] 
    #print(pianoroll.shape) 
      # Calculate the total measures
    n_total_measures = multitrack.get_max_length() // settings.measure_resolution
    candidate = n_total_measures - settings.n_measures
    target_n_samples = min(n_total_measures // settings.n_measures, settings.n_samples_per_song)
    stepsPerSample = settings.n_measures * settings.measure_resolution
      # Randomly select a number of phrases from the multitrack pianoroll
    for idx in range(7):   #np.random.choice(candidate, target_n_samples, False):
        start = idx * settings.measure_resolution
        end = (idx + settings.n_measures) * settings.measure_resolution
        # Skip the samples where some track(s) has too few notes
        if (pianoroll.sum(axis=(1, 2)) < 10).any():
            continue
        dataS.append(pianoroll[:, start:end])
  # Stack all the collected pianoroll segments into one big array
  #random.shuffle(dataS)
  dataS = np.stack(dataS)
  print(f"Successfully collect {len(dataS)} samples from {len(data)} songs")
  print(f"Data shape : {dataS.shape}")
  print(dataS.shape)

  return dataS