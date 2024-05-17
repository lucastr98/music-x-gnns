import pytube
import json
import pandas as pd
import ast
import os
from pytube.innertube import _default_clients

remainder_idx = [75, 739, 947, 1001, 1265, 1271, 1393, 2073, 2121, 2358, 2542,
                 2544, 2624, 2665, 2966, 3482, 3502, 3545, 4084, 4470, 4710,
                 5155, 5190, 5541, 5631, 6447, 6971, 7120, 7291, 7339, 7378,
                 7423, 7899, 7979, 7986, 8101, 8146, 8597, 8842, 9167, 9259,
                 9408, 9468, 9587, 9598, 9635, 9821, 10130, 10394, 10893, 11075,
                 11132, 11283, 11597, 11869, 12232, 12300, 12521, 12529, 13078,
                 13698, 13775, 14197, 14303, 14304, 14437, 14570, 14661, 14847,
                 15380, 16231, 16404, 16448, 17025, 17493, 17554, 17619]

olga_df = pd.read_csv("data/olga/olga.csv", index_col="index")
olga_df['tracks'] = olga_df['tracks'].apply(ast.literal_eval)

track_set = set()
duplicate_set = set()
for index, row in olga_df.iterrows():
  for mbid in row['tracks']:
    if mbid in track_set:
      duplicate_set.add(mbid)
    else:
      track_set.add(mbid)

for index, row in olga_df.iterrows():
  if index not in remainder_idx:
    continue
  print(index)

  mp3_exists = False
  _default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]
  for mbid in row['tracks']:
    # skip if duplicate mbid
    if mbid in duplicate_set:
      continue
    filename = f'data/jsons/ab-low-level-olga/low-level_{mbid}.json'
    if os.path.isfile(filename):
      with open(filename, 'r') as file:
        data = json.load(file)
        artist = data.get('metadata', {}).get('tags', {}).get('artist', [None])[0]
        title = data.get('metadata', {}).get('tags', {}).get('title', [None])[0]
        if (artist is None) or (title is None):
          continue
        
        # search YouTube
        s = pytube.Search(f"{artist} {title}")
        if len(s.results) == 0:
          continue
        yt = s.results[0]
    
        try:
          stream = yt.streams.filter(only_audio=True).first()
          stream.download(output_path='./data/remainder_mp3', filename=f'{mbid}.mp3')
          mp3_exists = True
          break
        except Exception as e:
          pass
  if not mp3_exists:
    print(f"No MP3 found for artist {row['musicbrainz_id']} with index {index}")
