import pytube
import json
import pandas as pd
import ast
import os
import glob
from pytube.innertube import _default_clients

df1 = pd.read_csv('data/am-ids_relatedArtists_songs_no_features.csv', index_col='id', usecols=['id', 'artist_id', 'songs'])
df1 = df1[~df1['songs'].isna()]
df1['songs'] = df1['songs'].apply(ast.literal_eval)
df1['songs'] = df1['songs'].apply(lambda x: [song[0] for song in x])

df2 = pd.read_csv('data/songs_am-ids_mb-ids.csv', index_col='id')
df2 = df2[~df2['musicbrainz_ids'].isna()]
df2['musicbrainz_ids'] = df2['musicbrainz_ids'].apply(ast.literal_eval)

tuple_lst = []
for index, row in df1.iterrows():
  print(index)

  mp3_exists = False
  _default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]
  for amid in row['songs']:
    mbid_lst = df2[df2['allmusic_id'] == amid]['musicbrainz_ids'].values
    if len(mbid_lst) == 0:
      continue
    for mbid in mbid_lst[0]:
      if glob.glob(f'data/mp3/*{mbid}.mp3'):
        mp3_exists = True
        tuple_lst.append((row['artist_id'], mbid))
        break
      filename = f'data/jsons/ab-low-level/low-level_{mbid}.json'
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
            stream.download(output_path='./data/disco-olga_mp3', filename=f'{mbid}.mp3')
            mp3_exists = True
            tuple_lst.append((row['artist_id'], mbid))
            break
          except Exception as e:
            pass
    if mp3_exists:
      break
  if not mp3_exists:
    print(f"No MP3 found for artist {row['artist_id']} with index {index}")

with open('data/disco-olga_tuples.txt', 'w') as f:
  for line in tuple_lst:
    f.write(f"{line}\n")
