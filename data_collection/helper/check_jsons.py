import os
import pandas as pd
import ast

df = pd.read_csv('../../data/songs_am-ids_mb-ids.csv', index_col='id')

# song ids where no musicbrainz id was found
ids_no_mb = df[df['musicbrainz_ids'].isna()]['allmusic_id'].to_list()

# song ids where musicbrainz id was found and either acousticbrainz low-level
# features were found as well or not found
ids_no_ab = []
ids_ab = []
songs = df[~df['musicbrainz_ids'].isna()]
songs['musicbrainz_ids'] = songs['musicbrainz_ids'].apply(ast.literal_eval)
for idx, row in songs.iterrows():
  ab_ll_found = False
  for mbid in row['musicbrainz_ids']:
    filename = f'../../data/jsons/ab-low-level/low-level_{mbid}.json'
    if os.path.isfile(filename):
      ab_ll_found = True
      ids_ab.append(row['allmusic_id'])
      break
  if not ab_ll_found:
    ids_no_ab.append(row['allmusic_id'])

artists_success = []
artists_no_song = []
artists_no_mb = []
artists_no_ab = []
df2 = pd.read_csv('../../data/dataset/song-am-id_2_artist-am-id.csv')
artist_2_songs = df2.groupby('artist_id').agg(list)
for idx, row in artist_2_songs.iterrows():
  success = False
  no_mb = False
  no_ab = False
  for id in row['song_id']:
    if id in ids_no_mb:
      no_mb = True
    elif id in ids_no_ab:
      no_ab = True
    elif id in ids_ab:
      success = True
    else:
      print("shouldn't be here")
  if success:
    artists_success.append(idx)
  elif no_ab:
    artists_no_ab.append(idx)
  elif no_mb:
    artists_no_mb.append(idx)
  else:
    print("shouldn't be here")


df2 = pd.read_csv('../../data/dataset/similar-to_edges.csv')
s1 = set(df2['from_id'].unique())
s2 = set(df2['to_id'].unique())
s = s1.union(s2)
df3 = pd.read_csv('../../data/dataset/artist-am-id_2_artist-name.csv').drop(['name'], axis=1)
no_relation_no_low_level = []
for idx, row in df3.iterrows():
  if row['id'] not in s and row['id'] not in artists_success:
    no_relation_no_low_level.append(row['id'])

print("total number of artists:                                           ", len(df3))
print("number of artists with song low-level features:                    ", len(artists_success))
print("number of artists with mb-song-ids but no ab-low-level-features:   ", len(artists_no_ab))
print("number of artists with songs on allmusic but no mb-song-ids:       ", len(artists_no_mb))
print("number of artists with no songs on allmusic:                       ", len(df3) - len(artist_2_songs))
print("number of artists that participate in at least one relation (edge):", len(s))
print("number of artists that with no relation and no low-level features: ", len(no_relation_no_low_level))