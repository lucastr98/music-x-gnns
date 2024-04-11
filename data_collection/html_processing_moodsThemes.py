import pandas as pd
from bs4 import BeautifulSoup

aids = pd.read_csv('../data/am-ids.csv', index_col='id')

moods_list = []
themes_list = []
for idx, row in aids.iterrows():
  print(f"Row {idx+1}")
  
  # open html
  with open(f'../data/htmls/moodsThemes/moodsThemes_{row["allmusic_id"]}.html', 'r', encoding='utf-8') as file:
    html = file.read()
  soup = BeautifulSoup(html, 'html.parser')

  # get moods
  try:
    moods_raw = soup.find("div", id="moodsGrid").select('a')
    moods = [(mood.get('href')[-12:], mood.get('title')) for mood in moods_raw]
  except AttributeError:
    moods = None
  if not moods:
    moods = None
  moods_list.append(moods)

  try:
    themes_raw = soup.find("div", id="themesGrid").select('a')
    themes = [(theme.get('href')[-12:], theme.get('title')) for theme in themes_raw]
  except AttributeError:
    themes = None
  if not themes:
    themes = None
  themes_list.append(themes)

aids = aids.rename(columns={'allmusic_id': 'artist_id'})
aids['moods'] = moods_list
aids['themes'] = themes_list
aids.to_csv('../data/am-ids_moodsThemes.csv')
