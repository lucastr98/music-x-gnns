import pandas as pd
import requests
import time
import ast

def get_low_level_json(id):
  time.sleep(1.05)
  response = requests.get(f'https://acousticbrainz.org/api/v1/{id}/low-level')
  if response.status_code == 200:
    return response.text
  elif response.status_code == 503:
    print("Server overloaded. Retrying after 5 seconds...")
    time.sleep(5)
    return get_low_level_json(id)
  else:
    return None

if __name__ == '__main__':
  songs = pd.read_csv('../data/songs_am-ids_mb-ids_100_artists_sample.csv', index_col='id')

  songs = songs[~songs['musicbrainz_ids'].isna()]
  songs['musicbrainz_ids'] = songs['musicbrainz_ids'].apply(ast.literal_eval)

  for idx, row in songs.iterrows():
    some_worked = False
    for mbid in row['musicbrainz_ids']:
      json = get_low_level_json(mbid)
      if json != None:
        some_worked = True
        f = open(f'../data/jsons/ab-low-level/low-level_{mbid}.json', "w")
        f.write(json)
        f.close()
        break
    if not some_worked:
      print(idx)
