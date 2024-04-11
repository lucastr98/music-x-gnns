import pandas as pd
import requests
import time

def get_allmusic_id(artist_id):
  response = requests.get(f'https://musicbrainz.org/ws/2/artist/{artist_id}?inc=url-rels&fmt=json')
  if response.status_code == 200:
    data = response.json()
    refs = [r['url']['resource'] for r in data['relations'] if r['type'] == 'allmusic']        
    allmusic_id = refs[0] if len(refs) != 0 else None
    name = data.get('name')
    return name, allmusic_id
  elif response.status_code == 503:
    print("Server overloaded. Retrying after 1 seconds...")
    time.sleep(1)
    return get_allmusic_id(artist_id)
  else:
    print(f"Failed to fetch data for artist {artist_id}. Status code: {response.status_code}")
    return None, None

data = pd.read_csv('olga.csv')
musicbrainz_ids = data['musicbrainz_id']
result = []
counter = 0
for id in musicbrainz_ids:
  time.sleep(1.05)
  counter += 1
  print(f"processing {counter}")
  name, allmusic_id = get_allmusic_id(id)
  if allmusic_id != None:
    allmusic_id = allmusic_id[-12:]
  result.append({'musicbrainz_id': id, 'name': name, 'allmusic_id': allmusic_id})
  if counter % 100 == 0:
    df = pd.DataFrame(result)
    df.to_csv(f'musicbrainz_api_out/out{int(counter / 100)}.csv')
    result = []
