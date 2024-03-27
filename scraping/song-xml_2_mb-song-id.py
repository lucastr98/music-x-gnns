import os
from bs4 import BeautifulSoup
import pandas as pd

def sorter(a):
  if not a[1]:
    return 1
  return a[1]

def get_ordered_id_list(mbid_year_list):
  first_not_none = None
  for i in range(len(mbid_year_list)):
    if mbid_year_list[i][1]:
      first_not_none = i
      break
  
  if first_not_none:
    mbid_year_list[0], mbid_year_list[first_not_none] = mbid_year_list[first_not_none], mbid_year_list[0]
  
  return [mbid_year[0] for mbid_year in mbid_year_list]

def get_year(recording):
  date = recording.find('first-release-date')
  if date:
    return int(date.text[:4]) if len(date.text) >= 4 else None
  
  release_list = recording.find('release-list')
  if release_list:
    release = release_list.find('release')
    if release:
      date = release.find('date')
      if date:
        return int(date.text[:4]) if len(date.text) >= 4 else None

      release_event_list = release.find('release-event-list')
      if release_event_list:
        date = release_event_list.find('date')
        if date:
          return int(date.text[:4]) if len(date.text) >= 4 else None

  return None

if __name__ == '__main__':
  # songs = pd.read_csv('../data/songs_100_artists_sample.csv', index_col='id')
  songs = pd.read_csv('../data/songs_100_artists_sample.csv')

  am_mb_mappings = []
  for idx, row in songs.iterrows():
    print(f"Index {idx}")

    mbid_year_list = []
    # with open(f'../data/xmls/songs/song_{row["song_id"]}.xml', 'r') as f:
    with open(f'../data/xmls/songs/mb-song-id_search_{row["song_id"]}.xml', 'r') as f:
      data = f.read()
      bs_data = BeautifulSoup(data, 'xml')

      for recording in bs_data.find_all('recording'):
        if recording.get('ns2:score') == '100':
          mbid_year_list.append((recording.get('id'), get_year(recording)))
    mbid_year_list = sorted(mbid_year_list, key=lambda x: (x[1] is not None, x[1]))
    am_mb_mappings.append((idx, row['song_id'], get_ordered_id_list(mbid_year_list) if mbid_year_list else None))

  df = pd.DataFrame(am_mb_mappings, columns=['id', 'allmusic_id', 'musicbrainz_ids'])
  df.to_csv('../data/songs_am-ids_mb-ids_100_artists_sample.csv', index=False)
