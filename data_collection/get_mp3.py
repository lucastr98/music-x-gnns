import pytube
import json
import pandas as pd
import ast
import os

failed_idx = [1001, 1393, 2073, 2624, 2793, 4084, 5541, 6447, 6971, 7899, 7986, 8146, 8842, 9167, 9408, 9598, 9635, 9893, 10394, 11132, 11283, 11597, 12521, 13078, 13698, 14197, 14303, 14847, 15380, 16231, 17554, 17619]

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
  if index < 0:
    continue
  if index in failed_idx:
    continue

  track_found = False
  mp3_exists = False
  for mbid in row['tracks']:
    # skip if duplicate mbid
    if mbid in duplicate_set:
      continue
    # skip if already exists
    if os.path.isfile(f'data/mp3/{mbid}.mp3'):
      mp3_exists = True
      break
    filename = f'data/jsons/ab-low-level-olga/low-level_{mbid}.json'
    if os.path.isfile(filename):
      with open(filename, 'r') as file:
        data = json.load(file)
        artist = data.get('metadata', {}).get('tags', {}).get('artist', [None])[0]
        title = data.get('metadata', {}).get('tags', {}).get('title', [None])[0]
        length = data.get('metadata', {}).get('audio_properties', {}).get('length', None)
        if (artist is None) or (title is None):
          continue
        track_found = True
        break
  
  if mp3_exists:
    continue
  elif track_found:
    s = pytube.Search(f"{artist} {title}")
    yt = s.results[0]
    
    yt_length = yt.length
    ab_length = int(length)
    if abs(yt_length - ab_length) > 10:
      print(f"large difference in length for track {mbid} of artist {row['musicbrainz_id']}")

    stream = yt.streams.filter(only_audio=True).first()
    stream.download(output_path='./data/new_mp3', filename=f'{mbid}.mp3')
  else:
    print(f"no unique track found on youtube for artist {row['musicbrainz_id']} (idx: {index})")
