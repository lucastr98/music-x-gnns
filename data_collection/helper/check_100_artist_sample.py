import pandas as pd
from pathlib import Path
import ast
import numpy as np


df1 = pd.read_csv('../data/songs_100_artists_sample.csv')
df2 = pd.read_csv('../data/songs_am-ids_mb-ids_100_artists_sample.csv', index_col='id')
dfs = pd.merge(df1, df2, left_on='song_id', right_on='allmusic_id')
# dfs['mb_bool'] = dfs['musicbrainz_ids'].isna()

mask = ~dfs['musicbrainz_ids'].isna()
dfs.loc[mask, 'musicbrainz_ids'] = dfs[mask]['musicbrainz_ids'].apply(ast.literal_eval)

ab_bool_list = []
mb_bool_list = []
for idx, row in dfs.iterrows():
  if not isinstance(row['musicbrainz_ids'], list):
    mb_bool_list.append(False)
    ab_bool_list.append(False)
    continue
  
  mb_bool_list.append(True)
  exists = False
  for mbid in row['musicbrainz_ids']:
    if Path(f'../data/jsons/ab-low-level/low-level_{mbid}.json').is_file():
      exists = True
      break
  ab_bool_list.append(exists)

dfs['ab_bool'] = ab_bool_list
dfs['mb_bool'] = mb_bool_list

bool_df = dfs[['artist_id', 'ab_bool', 'mb_bool']]
artists_grouped_df = bool_df.groupby('artist_id').agg({'ab_bool': 'any', 'mb_bool': 'any'})

print(artists_grouped_df['mb_bool'].sum())
print(artists_grouped_df['ab_bool'].sum())
