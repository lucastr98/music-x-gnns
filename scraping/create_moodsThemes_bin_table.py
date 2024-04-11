import pandas as pd

all_moods = pd.read_csv('../data/dataset/moods_am-id_2_name.csv')
all_themes = pd.read_csv('../data/dataset/themes_am-id_2_name.csv')
all_artists = pd.read_csv('../data/dataset/artists_am-id_2_name.csv')
artist_2_mood = pd.read_csv('../data/dataset/artist-am-id_2_mood-am-id.csv')
artist_2_theme = pd.read_csv('../data/dataset/artist-am-id_2_theme-am-id.csv')

moods_lst = sorted(all_moods['id'].to_list())
themes_lst = sorted(all_themes['id'].to_list())
artists_lst = all_artists['id'].to_list()

bin_lst = []
i = 0
for aid in artists_lst:
  artist_moods = artist_2_mood[artist_2_mood['artist_id'] == aid]['mood_id'].to_list()
  bin = [mood in artist_moods for mood in moods_lst]
  bin.insert(0, aid)
  artist_themes = artist_2_theme[artist_2_theme['artist_id'] == aid]['theme_id'].to_list()
  themes_bin = [theme in artist_themes for theme in themes_lst]
  bin.extend(themes_bin)
  bin_lst.append(bin)
  i += 1

df_cols = moods_lst
df_cols.insert(0, 'artist_id')
df_cols.extend(themes_lst)
df = pd.DataFrame(bin_lst, columns=df_cols)

df.to_csv('../data/dataset/am-id_2_moodsThemes.csv', index=False)
