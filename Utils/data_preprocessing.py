import pypianoroll
import numpy as np
import torch


from pypianoroll.track import BinaryTrack
from torch.utils.data import Dataset
from torch import Tensor
from typing import Tuple



import settings

"""Midi dataset."""

class MidiDataset(Dataset):
    """MidiDataset.
    Parameters
    ----------
    path: str
        Path to dataset.
    split: str, optional (default="train")
        Split of dataset.
    n_bars: int, optional (default=2)
        Number of bars.
    n_steps_per_bar: int, optional (default=16)
        Number of steps per bar.
    """

    def __init__(
        self,
        path: str,
        split: str = "train",
        n_bars: int = 8,
        n_steps_per_bar: int = 16,
    ) -> None:
        """Initialize."""
        self.n_bars = n_bars
        self.n_steps_per_bar = n_steps_per_bar
        dataset = np.load(path, allow_pickle=True, encoding="bytes")[split]
        self.data_binary, self.data_ints, self.data = self.__preprocess__(dataset)

    def __len__(self) -> int:
        """Return the number of samples in dataset."""
        return len(self.data_binary)

    def __getitem__(self, index: int) -> Tensor:
        """Return one samples from dataset.
        Parameters
        ----------
        index: int
            Index of sample.
        Returns
        -------
        Tensor:
            Sample.
        """
        return torch.from_numpy(self.data_binary[index]).float()

    def __preprocess__(self, data: np.ndarray) -> Tuple[np.ndarray]:
        """Preprocess data.
        Parameters
        ----------
        data: np.ndarray
            Data.
        Returns
        -------
        Tuple[np.ndarray]:
            Data binary, data ints, preprocessed data.
        """
        data_ints = []
        for x in data:
            skip = True
            skip_rows = 0
            while skip:
                if not np.any(np.isnan(x[skip_rows: skip_rows + 4])):
                    skip = False
                else:
                    skip_rows += 4
            if self.n_bars * self.n_steps_per_bar < x.shape[0]:
                data_ints.append(x[skip_rows: self.n_bars * self.n_steps_per_bar + skip_rows, :])
        
        data_ints = np.array(data_ints)

        self.n_songs = data_ints.shape[0]
        self.n_tracks = data_ints.shape[2]
        data_ints = data_ints.reshape([self.n_songs, self.n_bars * self.n_steps_per_bar, self.n_tracks])
        max_note = settings.n_pitches
        mask = np.isnan(data_ints)
        data_ints[mask] = max_note + 1
        max_note = max_note + 1
        data_ints = data_ints.astype(int)
        
        num_classes = max_note + 1
        data_binary = np.eye(num_classes)[data_ints]
        data_binary[data_binary == 0] = -1
        data_binary = np.delete(data_binary, max_note, -1)
        data_binary = data_binary.transpose([0, 1, 3, 2])

        return data_binary, data_ints, data
        

from pypianoroll.track import BinaryTrack
def save_pianoroll_as_midi(dataset,
                  programs=settings.programs,
                  track_names=settings.track_names,
                  is_drums=settings.is_drums,
                  tempo=settings.tempo,           # in bpm
                  beat_resolution=settings.beat_resolution,  # number of time steps
                  ):
    data_ = []
    sopData = []

    for piece in dataset:

      pianoroll = piece > 0

      #print(pianoroll.shape)

    # Reshape batched pianoroll array to a single pianoroll array
      pianoroll_ = pianoroll.reshape((-1, pianoroll.shape[1], pianoroll.shape[2]))

      #print(pianoroll_.shape)

    # Create the tracks   
      tracks = []
      for idx in range(pianoroll_.shape[2]):
          tracks.append(pypianoroll.BinaryTrack(
            track_names[idx], programs[idx], is_drums[idx], pianoroll_[..., idx]))
          
      multitrack = pypianoroll.Multitrack(
          tracks=tracks, tempo=settings.tempo_array, resolution=beat_resolution)
      
      data_.append(multitrack)

      melody = []
      for idx in range(1):
        melody.append(pypianoroll.BinaryTrack(
            track_names[idx], programs[idx], is_drums[idx], pianoroll_[..., idx]))
        
        sMultitrack = pypianoroll.Multitrack(
          tracks=melody, tempo=settings.tempo_array, resolution=beat_resolution)
        
        sopData.append(sMultitrack)
        

    return data_, sopData
