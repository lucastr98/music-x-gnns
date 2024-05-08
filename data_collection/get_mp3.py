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

  for mbid in row['tracks']:
    filename = f'data/jsons/ab-low-level-olga/low-level_{mbid}.json'
    if os.path.isfile(filename):
      with open(filename, 'r') as file:
        data = json.load(file)
      break
  artist = data['metadata']['tags']['artist'][0]
  title = data['metadata']['tags']['title'][0]
  length = data['metadata']['audio_properties']['length']

  s = pytube.Search(f"{artist} {title}")
  yt = s.results[0]
  yt_length = yt.length
  ab_length = int(length)
  if abs(yt_length - ab_length) > 10:
    print(f"large difference in length for track {mbid} of artist {row['musicbrainz_id']}")

  stream = yt.streams.filter(only_audio=True).first()
  stream.download(output_path='./data/mp3', filename=f'{mbid}.mp3')
