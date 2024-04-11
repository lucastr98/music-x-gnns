import pandas as pd
import os

df = pd.read_csv('../../data/songs_no_features.csv', index_col='id')

last_idx = -1
for idx, row in df.iterrows():
  if last_idx + 1 < idx:
    print(last_idx, idx)
  last_idx = idx
  filename = '../../data/xmls/songs/mb-song-id_search_' + row['song_id'] + '.xml'
  if not os.path.isfile(filename):
    print(idx)
