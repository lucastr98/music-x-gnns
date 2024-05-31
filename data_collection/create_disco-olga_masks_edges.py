import pandas as pd
import numpy as np
import ast
import scipy.sparse

# load data
df = pd.read_csv("../data/disco-olga_complete.csv")

# split masks
for split in ['train', 'val', 'test']:
  mask = np.array(df[df['partition'] == split].index)
  np.save(f'../data/disco-olga/{split}_mask.npy', mask)

# edges
allmusic_ids = df['artist_am-id'].tolist()
for edge_type in ['similar_to', 'influenced_by', 'followed_by', 'associated_with', 'collaborated_with']:
  relations_df = df[['artist_am-id', edge_type]]
  relations_df = relations_df[~relations_df[edge_type].isna()]
  relations_df[edge_type] = relations_df[edge_type].apply(ast.literal_eval)

  edges = set()
  for idx1, row in relations_df.iterrows():
    for related_id in row[edge_type]:
      if related_id in allmusic_ids:
        idx2 = allmusic_ids.index(related_id)
        new_edge = (idx1, idx2) if idx1 < idx2 else (idx2, idx1)
        edges.add(new_edge)
  print(f"number of {edge_type} edges: {len(edges)}")

  data = np.full(len(edges), True)
  row_indices, col_indices = [], []
  for idx1, idx2 in edges:
    row_indices.append(idx1)
    col_indices.append(idx2)
  csr = scipy.sparse.csr_matrix((data, (row_indices, col_indices)), shape=(len(allmusic_ids), len(allmusic_ids))) 
  scipy.sparse.save_npz(f'../data/disco-olga/{edge_type}.npz', csr)
