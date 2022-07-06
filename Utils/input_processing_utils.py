from tqdm import tqdm
import pypianoroll
from pypianoroll import Multitrack, Track

from Utils import settings_utils



def Get_Samples(data: list):

  dataS = []
  for multitrack in tqdm(data):
    
    multitrack.binarize()
      # Downsample the pianorolls (shape: n_timesteps x n_pitches)
    multitrack.set_resolution(beat_resolution)
      # Stack the pianoroll (shape: n_tracks x n_timesteps x n_pitches)
    pianoroll = (multitrack.stack() > 0)
    
      # Get the target pitch range only
    pianoroll = pianoroll[:, :, lowest_pitch:lowest_pitch + (n_pitches + 1)] 
    #print(pianoroll.shape) 
      # Calculate the total measures
    n_total_measures = multitrack.get_max_length() // measure_resolution
    candidate = n_total_measures - n_measures
    target_n_samples = min(n_total_measures // n_measures, n_samples_per_song)
    stepsPerSample = n_measures * measure_resolution
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

input("press any key")

