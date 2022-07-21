import pypianoroll
import numpy as np
import matplotlib.pyplot as plt
import os, os.path, shutil

import settings

def Show_History(history_samples: dict, train_out_dir: str, train_out_dir_p: str):
# Show history
	steps = [0, settings.sample_interval, 10 * settings.sample_interval, 100 * settings.sample_interval, settings.n_steps]
	for step in steps:
		print(f"Step={step}")
		samples = history_samples[step].transpose(1, 0, 2, 3).reshape(settings.n_tracks, -1, (settings.n_pitches+1))
		tracks = []
		for idx, (program, is_drum, track_name) in enumerate(zip(settings.programs, settings.is_drums, settings.track_names)):
			pianoroll = np.pad(
				samples[idx] > 0.5,
				((0, 0), (settings.lowest_pitch, 128 - settings.lowest_pitch - (settings.n_pitches+1)))
			)
			tracks.append(
				pypianoroll.BinaryTrack(
					name=track_name,
					program=program,
					is_drum=is_drum,
					pianoroll=pianoroll,
				)
			)
		
		m = pypianoroll.Multitrack(tracks=tracks, tempo=settings.tempo_array, resolution=settings.beat_resolution)

		m.write(os.path.join(train_out_dir, 'midiforstep %s.mid' % step))
		
		m.binarize()
		m.set_resolution(settings.beat_resolution)

		axs = m.plot()
		for ax in axs:
			for x in range(
				settings.measure_resolution,
				4 * settings.measure_resolution * settings.n_measures,
				settings.measure_resolution
			):
				if x % (settings.measure_resolution * 4) == 0:
					ax.axvline(x - 0.5, color='k')
				else:
					ax.axvline(x - 0.5, color='k', linestyle='-', linewidth=1)
		plt.gcf().set_size_inches((16, 8))
		plt.savefig(os.path.join(train_out_dir_p, 'pianorollforstep%s.png' % step))
		plt.show()
