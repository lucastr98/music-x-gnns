import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

chrome_options = Options()
chrome_options.add_argument("--headless")

def get_html(driver, aid):
  driver.get(f'https://www.allmusic.com/artist/{aid}#relatedArtists')
  try:
    # Wait until sidebarNav is present (always the case)
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, 'sidebarNav'))
    )

    # check if relatedArtistsSidebarLink is present
    if driver.find_elements(By.ID, 'relatedArtistsSidebarLink'):
      # wait for one of the related artists classes
      WebDriverWait(driver, 10).until(
        lambda driver: driver.find_element(By.CSS_SELECTOR, 
            ".related.similars.clearfix, \
             .related.influencers.clearfix, \
             .related.followers.clearfix, \
             .related.associatedwith.clearfix, \
             .related.collaboratorwith.clearfix")
      )
  except TimeoutException:
    # sidebarNav not found
    print("sidebarNav not present.")
  finally:
    return driver.page_source

if __name__ == '__main__':
  driver = webdriver.Chrome(options=chrome_options)
  aids = pd.read_csv('../data/am-ids_only_clean.csv', index_col='id')
  total_rows = aids.shape[0]
  for index, row in aids.iterrows():
    print(f"Row {index+1}/{total_rows}")
    aid = row['allmusic_id']

    html = get_html(driver, aid)

    f = open(f'../data/htmls/relatedArtists_{aid}.html', "w")
    f.write(html)
    f.close()


  driver.quit()
