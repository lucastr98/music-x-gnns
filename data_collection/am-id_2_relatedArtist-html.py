import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import signal

MIN_ID = 16001
MAX_ID = 17000

driver = None
chrome_options = Options()
chrome_options.add_argument("--headless")

def signal_handler(sig, frame):
  print('You pressed Ctrl+C! Closing WebDriver and exiting.')
  if driver is not None:
    driver.quit()  # Make sure to quit the driver to close the browser window
  sys.exit(0)

def get_html(driver, aid):
  driver.get(f'https://www.allmusic.com/artist/{aid}#relatedArtists')
  try:
    # Wait until sidebarNav is present (always the case)
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, 'sidebarNav'))
    )
  except TimeoutException:
    print("  sidebarNav not found", end="")
    return None

  # check if relatedArtistsSidebarLink is present
  if driver.find_elements(By.ID, 'relatedArtistsSidebarLink'):
    # wait for one of the related artists classes
    try:
      WebDriverWait(driver, 10).until(EC.any_of(
          EC.presence_of_element_located((By.CSS_SELECTOR, '.related.similars.clearfix')),
          EC.presence_of_element_located((By.CSS_SELECTOR, '.related.influencers.clearfix')),
          EC.presence_of_element_located((By.CSS_SELECTOR, '.related.followers.clearfix')),
          EC.presence_of_element_located((By.CSS_SELECTOR, '.related.associatedwith.clearfix')),
          EC.presence_of_element_located((By.CSS_SELECTOR, '.related.collaboratorwith.clearfix'))
        )
      )
    except TimeoutException:
      print("  no related artists class found", end="")
      return None

  return driver.page_source

if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal_handler)
  driver = webdriver.Chrome(options=chrome_options)
  aids = pd.read_csv('../data/am-ids_only_cleaner.csv', index_col='id')
  for index, row in aids.iterrows():
    if index < MIN_ID:
      continue
    elif index > MAX_ID:
      break
    print(f"Index {index}/{MAX_ID}")
    aid = row['allmusic_id']

    html = get_html(driver, aid)
    count = 1
    while (html == None):
      print(f': retry {count}/10')
      html = get_html(driver, aid)
      if count >= 10 and html == None:
        print(f':  all retries failed')
        break
      count = count + 1

    if html != None:
      f = open(f'../data/htmls/relatedArtists/relatedArtists_{aid}.html', "w")
      f.write(html)
      f.close()

  driver.quit()
