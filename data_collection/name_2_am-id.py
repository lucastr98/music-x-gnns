import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-images")

num_files = 1

def get_artist_link(name):
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(f'https://www.allmusic.com/search/artists/{name}')
  html = driver.page_source
  driver.quit()
  soup = BeautifulSoup(html, 'html.parser')
  try:
    link = soup.select_one('.name a').get('href')
    return link
  except AttributeError:
    return None

if __name__ == '__main__':
  for i in range(num_files):
    print(f"File {i+1}/{num_files}")
    data = pd.read_csv('../data/musicbrainz_id_2_allmusic_id.csv', index_col='id')
    for index, row in data.iterrows():
      print(f"    Row {index+1}/{data.shape[0]}")
      if isinstance(row['allmusic_id'], str):
        continue
      allmusic_id = get_artist_link(row['name'])
      if allmusic_id != None:
        allmusic_id = allmusic_id[-12:]
      row['allmusic_id'] = allmusic_id
    data.to_csv(f"allmusic_ids/out{i+1}.csv")