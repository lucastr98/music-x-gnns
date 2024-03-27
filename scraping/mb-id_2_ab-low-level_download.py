import pandas as pd
import requests
import tarfile
import zstandard as zstd
import os
import ast
import shutil

def download_file(url, local_filename):
  with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
      for chunk in r.iter_content(chunk_size=8192):
        if chunk:  # filter out keep-alive new chunks
          f.write(chunk)

def decompress_zstd(zstd_file, output_file):
  with open(zstd_file, 'rb') as compressed:
    with open(output_file, 'wb') as decompressed:
      dctx = zstd.ZstdDecompressor()
      decompressed.write(dctx.stream_reader(compressed).read())
  os.remove(zstd_file)  # Optionally remove the compressed file

def extract_tar(tar_file):
  with tarfile.open(tar_file, 'r') as tar:
    tar.extractall(path='.')
  os.remove(tar_file)  # Optionally remove the tar file after extraction

def download_uncompress(num):
  url = f'https://data.metabrainz.org/pub/musicbrainz/acousticbrainz/dumps/acousticbrainz-lowlevel-json-20220623/acousticbrainz-lowlevel-json-20220623-{num}.tar.zst'
  zstd_file = f'data/acousticbrainz-lowlevel-json-{num}.tar.zst'
  tar_file = f'data/acousticbrainz-lowlevel-json-{num}.tar'
  download_file(url, zstd_file)
  decompress_zstd(zstd_file, tar_file)
  extract_tar(tar_file)

def get_jsons(songs, num):
  for idx, row in songs.iterrows():
    print(f"  File {num}: Index {idx}")
    for mbid in row['musicbrainz_ids']:
      filename = f'data/acousticbrainz-lowlevel-json-{num}/lowlevel/{mbid[:2]}/{mbid[2]}/{mbid}-0.json'
      if os.path.isfile(filename):
        shutil.copyfile(filename, 'data/jsons/ab-low-level/low-level_{mbid}.json')
        break

def cleanup(num):
  shutil.rmtree(f'data/accousticbrainz-lowlevel-json-{num}')

if __name__ == "__main__":
  songs = pd.read_csv('data/songs_am-ids_mb-ids.csv', index_col='id')
  songs = songs[~songs['musicbrainz_ids'].isna()]
  songs['musicbrainz_ids'] = songs['musicbrainz_ids'].apply(ast.literal_eval)

  for i in range(0, 1):
    print(f"Starting Download of File {i}")
    download_uncompress(i)
    print("Download successful, starting JSON extraction")
    get_jsons(songs, i)
    print("JSON extraction done\n")
  