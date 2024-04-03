import pandas as pd
import requests
import tarfile
import zstandard as zstd
import os
import ast
import shutil
import subprocess

def download_file(url, local_filename):
  with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
      for chunk in r.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive new chunks
          f.write(chunk)

def decompress(zstd_file):
  tar_command = f"tar --use-compress-program=unzstd -xvf {zstd_file} -C data/"
  try:
    subprocess.run(tar_command, check=True, shell=True)
  except subprocess.CalledProcessError as e:
    print(f"An error occurred during decompression: {e}")

def download_decompress(num):
  url = f'https://data.metabrainz.org/pub/musicbrainz/acousticbrainz/dumps/acousticbrainz-lowlevel-json-20220623/acousticbrainz-lowlevel-json-20220623-{num}.tar.zst'
  zstd_file = f'data/acousticbrainz-lowlevel-json-{num}.tar.zst'
  download_file(url, zstd_file)
  decompress(zstd_file)

def get_jsons(songs, num):
  for idx, row in songs.iterrows():
    print(f"  File {num}: Index {idx}")
    mbid = row['tracks']
    filename = f'data/acousticbrainz-lowlevel-json-20220623/lowlevel/{mbid[:2]}/{mbid[2]}/{mbid}-0.json'
    if os.path.isfile(filename):
      shutil.copyfile(filename, f'data/jsons/ab-low-level/low-level_{mbid}.json')

def cleanup(num):
  shutil.rmtree(f'data/acousticbrainz-lowlevel-json-20220623')
  os.remove(f'data/acousticbrainz-lowlevel-json-{num}.tar.zst')

if __name__ == "__main__":
  songs = pd.read_csv('data/olga_songs_mb-artist-id_mb-track-id.csv', index_col='id')

  for i in range(0, 15):
    print(f"Starting Download of File {i}")
    download_decompress(i)
    print("Download successful, starting JSON extraction")
    get_jsons(songs, i)
    print("JSON extraction done, starting cleanup")
    cleanup(i)
    print(f"Cleanup for File {i} done\n")
  