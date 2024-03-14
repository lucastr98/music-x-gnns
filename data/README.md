# Data
Here the data that was generated to build our final dataset is described. The description of the files is ordered in creation time.
- `olga.csv`: the musicbrainz_ids of the artists the authors of the OLGA paper used in their dataset. It is provided [here](https://gitlab.com/fdlm/olga/).
- `mb-id_name_am-id_partial.csv`: musicbrainz_id with the name and the allmusic_id from the musicbrainz API. Incomplete because allmusic_id missing for about a third.
- `mb-id_name_am-id.csv`: musicbrainz_id with the name and the allmusic_id from the musicbrainz API. Complete because the last third was scraped from allmusic.
- `am-ids_only.csv`: allmusic_ids extracted from `mb-id_name_am-id.csv`.
- `am-ids_only_clean.csv`: allmusic_ids extracted from `mb-id_name_am-id.csv` with NaNs removed.
- `am-ids_only_cleaner.csv`: allmusic_ids extracted from `mb-id_name_am-id.csv` with NaNs and duplicates removed or replaced (in case of same id for two different names).
- `am-ids.csv`: `am-ids_only_cleaner.csv` with indices reset (now correspond no longer to the indices in `olga.csv`)
- `am-ids_relatedArtists.csv`: table holding all information gathered from the relatedArtists HTML files. 
  - artist_id (allmusic_id)
  - name (str)
  - similar_to (list of allmusic_id)
  - influenced_by (list of allmusic_id)
  - followed_by (list of allmusic_id)
  - associated_with (list of allmusic_id)
  - collaborated_with (list of allmusic_id)
- `edges.csv`: list of directed edges obtained from the artists listed under *Similar To* of a given artist. An edge is represented by two allmusic_ids.