import torch
import laion_clap
import pandas as pd
import os
import numpy as np
import sys

first_idx = int(sys.argv[1])
last_idx = int(sys.argv[2])

model = laion_clap.CLAP_Module(enable_fusion=False, amodel='HTSAT-base')
model.load_ckpt('data/music_audioset_epoch_15_esc_90.14.pt')

audio_file = []
mp3s = os.listdir('data/mp3/')
olga_df = pd.read_csv("data/olga/olga.csv", index_col="index")
for index, row in olga_df.iterrows():
  if index < first_idx:
    continue
  elif index > last_idx:
    break
  mbid = row['musicbrainz_id']
  for mp3 in mp3s:
    if mp3.startswith(mbid):
      audio_file.append(f'data/mp3/{mp3}')
      break

audio_embed = model.get_audio_embedding_from_filelist(x=audio_file, use_tensor=False)
print(audio_embed.shape)
np.save(f'data/olga/clap_{first_idx}_{last_idx}.npy', audio_embed)
