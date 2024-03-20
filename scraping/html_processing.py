import pandas as pd
from bs4 import BeautifulSoup

aids = pd.read_csv('../data/am-ids.csv', index_col='id')

name_list = []
similar_to_list = []
influenced_by_list = []
followed_by_list = []
associated_with_list = []
collaborated_with_list = []
songs_list = []
for index, row in aids.iterrows():
  print(f"Row {index+1}")

  # open related artists
  with open(f'../data/htmls/relatedArtists/relatedArtists_{row["allmusic_id"]}.html', 'r', encoding='utf-8') as file:
    html = file.read()
  soup = BeautifulSoup(html, 'html.parser')

  # name
  try:
    name = soup.find('h1', id='artistName').get_text()
  except AttributeError:
    name = None
  name_list.append(name)

  # similar to
  try:
    similar_to_xml = soup.select('.related.similars.clearfix a')
    similar_to = [xml.get('href')[-12:] for xml in similar_to_xml]
  except AttributeError:
    similar_to = None
  if not similar_to:
    similar_to = None
  similar_to_list.append(similar_to)

  # influenced by
  try:
    influenced_by_xml = soup.select('.related.influencers.clearfix a')
    influenced_by = [xml.get('href')[-12:] for xml in influenced_by_xml]
  except AttributeError:
    influenced_by = None
  if not influenced_by:
    influenced_by = None
  influenced_by_list.append(influenced_by)

  # followed by
  try:
    followed_by_xml = soup.select('.related.followers.clearfix a')
    followed_by = [xml.get('href')[-12:] for xml in followed_by_xml]
  except AttributeError:
    followed_by = None
  if not followed_by:
    followed_by = None
  followed_by_list.append(followed_by)

  # associated with
  try:
    associated_with_xml = soup.select('.related.associatedwith.clearfix a')
    associated_with = [xml.get('href')[-12:] for xml in associated_with_xml]
  except AttributeError:
    associated_with = None
  if not associated_with:
    associated_with = None
  associated_with_list.append(associated_with)

  # collaborated with
  try:
    collaborated_with_xml = soup.select('.related.collaboratorwith.clearfix a')
    collaborated_with = [xml.get('href')[-12:] for xml in collaborated_with_xml]
  except AttributeError:
    collaborated_with = None
  if not collaborated_with:
    collaborated_with = None
  collaborated_with_list.append(collaborated_with)

  with open(f'../data/htmls/songs/songs_{row["allmusic_id"]}.html', 'r', encoding='utf-8') as file:
    html = file.read()
  soup = BeautifulSoup(html, 'html.parser')

  # # songs
  # try:
  #   songs_xml = soup.select('.songTitle a')
  #   song_ids = [xml.get('href')[-12:] for xml in songs_xml]
  #   song_names = [xml.text for xml in songs_xml]
  #   songs = [(song_ids[i], song_names[i]) for i in range(0, len(song_ids))]
  # except AttributeError:
  #   songs = None
  # if not songs:
  #   songs = None
  # songs_list.append(songs)

  # songs without features
  try:
    songs = []
    songs_xml = soup.select('.singleSongResult')
    for song in songs_xml:
      title_element = song.select_one('.songTitle a')
      if title_element:
        song_title = title_element.text
        feat_artist = song.select_one('.songTitle .featuredArtists')
        if not feat_artist:
          song_id = title_element.get('href')[-12:]
          songs.append((song_id, song_title))
  except AttributeError:
    songs = None
  if not songs:
    songs = None
  songs_list.append(songs)

aids = aids.rename(columns={'allmusic_id': 'artist_id'})
aids['name'] = name_list
aids['similar_to'] = similar_to_list
aids['influenced_by'] = influenced_by_list
aids['followed_by'] = followed_by_list
aids['associated_with'] = associated_with_list
aids['collaborated_with'] = collaborated_with_list
aids['songs'] = songs_list
aids.to_csv('../data/am-ids_relatedArtists_songs_no_features.csv')
