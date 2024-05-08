import pytube
import json
import pandas as pd
import ast
import os

olga_df = pd.read_csv("data/olga/olga.csv", index_col="index")
olga_df['tracks'] = olga_df['tracks'].apply(ast.literal_eval)
for index, row in olga_df.iterrows():
  if index < 0:
    continue
  if index > 1000:
    break

  if index % 10 == 0:
    print(f"processing index {index}")

  length_available = True
  for mbid in row['tracks']:
    filename = f'data/jsons/ab-low-level-olga/low-level_{mbid}.json'
    if os.path.isfile(filename):
      with open(filename, 'r') as file:
        data = json.load(file)
        artist = data.get('metadata', {}).get('tags', {}).get('artist', [None])[0]
        title = data.get('metadata', {}).get('tags', {}).get('title', [None])[0]
        length = data.get('metadata', {}).get('audio_properties', {}).get('length', None)
        if (artist is None) or (title is None):
          continue
        elif length is None:
          length_available = False
        break

  s = pytube.Search(f"{artist} {title}")
  yt = s.results[0]
  
  if length_available:
    yt_length = yt.length
    ab_length = int(length)
    if abs(yt_length - ab_length) > 10:
      print(f"large difference in length for track {mbid} of artist {row['musicbrainz_id']}")
  else:
    print(f"length not available for track {mbid} of artist {row['musicbrainz_id']}")

  stream = yt.streams.filter(only_audio=True).first()
  stream.download(output_path='./data/mp3', filename=f'{mbid}.mp3')
