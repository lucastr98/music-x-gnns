import pandas as pd
import requests
from urllib.parse import quote
import time

def get_song_xml(query):
  response = requests.get(f'https://musicbrainz.org/ws/2/recording/?query={query}')
  if response.status_code == 200:
    return response.text
  elif response.status_code == 503:
    print("Server overloaded. Retrying after 5 seconds...")
    time.sleep(5)
    return get_song_xml(query)
  else:
    print("Error fetching data for the following query:")
    print(query)
    print()
    return None

if __name__ == '__main__':
  songs = pd.read_csv('../data/songs_sample.csv', index_col='id')
  
  for idx, row in songs.iterrows():
    print(idx)
    artist_name = quote(row['artist_name'], safe='')
    song_name = quote(row['song_name'], safe='')
    query = f'artist:{artist_name}%20AND%20recording:{song_name}'
    print(query)

    xml = get_song_xml(query)
    if xml != None:
      f = open(f'../data/xmls/songs/song_{row["song_id"]}.xml', "w")
      f.write(xml)
      f.close()

    time.sleep(1.05)
    
