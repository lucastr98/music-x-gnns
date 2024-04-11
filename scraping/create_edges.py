import pandas as pd
import numpy as np
import ast

relation = 'collaborated_with'

# load related artists data and only keep id and similar_to
related_artists_all = pd.read_csv('../data/am-ids_relatedArtists.csv', index_col='id')
related_artists = related_artists_all[['artist_id', relation]]
allmusic_ids = related_artists['artist_id'].tolist()

# remove all rows with no similar_to artists and turn others into list
related_artists = related_artists[~related_artists[relation].isna()]
related_artists[relation] = related_artists[relation].apply(ast.literal_eval)

# find (directed) edges
edges = []
artist_connection_cnt_list = []
for index, row in related_artists.iterrows():
  print(f"Index {index}")
  artist_connection_cnt = 0
  for related_id in row[relation]:
    if related_id in allmusic_ids:
      artist_connection_cnt += 1
      new_edge = (row['artist_id'], related_id)
      edges.append(new_edge)
  if artist_connection_cnt > 0:
    artist_connection_cnt_list.append(artist_connection_cnt)

print(f"Average number of connections per artist: {np.round(sum(artist_connection_cnt_list) / len(artist_connection_cnt_list), 2)} (artists with no connections not considered)")
edges_df = pd.DataFrame(edges, columns=['from_id', 'to_id'])
edges_df.to_csv(f'../data/dataset/{relation}_edges.csv', index=False)