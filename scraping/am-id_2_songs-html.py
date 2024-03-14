import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import signal

MIN_ID = 2001
MAX_ID = 3000

driver = None
chrome_options = Options()
chrome_options.add_argument("--headless")

def signal_handler(sig, frame):
  print('You pressed Ctrl+C! Closing WebDriver and exiting.')
  if driver is not None:
    driver.quit()  # Make sure to quit the driver to close the browser window
  sys.exit(0)

def get_html(driver, aid):
  driver.get(f'https://www.allmusic.com/artist/{aid}#songs')
  try:
    # Wait until sidebarNav is present (always the case)
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, 'sidebarNav'))
    )
  except TimeoutException:
    print("  sidebarNav not found", end="")
    return None

  # check if songsSidebarLink is present
  if driver.find_elements(By.ID, 'songsSidebarLink'):
    # wait for one of the songs classes
    try:
      WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'songTitle'))
      )
    except TimeoutException:
      print("  no song class found", end="")
      return None

  return driver.page_source

if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal_handler)
  driver = webdriver.Chrome(options=chrome_options)
  aids = pd.read_csv('../data/am-ids.csv', index_col='id')
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
      print(f': retry {count}/5')
      html = get_html(driver, aid)
      if count >= 5 and html == None:
        print(f':  all retries failed')
        break
      count = count + 1

    if html != None:
      f = open(f'../data/htmls/songs/songs_{aid}.html', "w")
      f.write(html)
      f.close()

  driver.quit()
