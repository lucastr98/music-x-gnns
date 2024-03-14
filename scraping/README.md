# Scraping
This is all the Code used to build the dataset (described in the data folder's `README`) we used. For building the dataset the musicbrainz API was used and the allmusic website was scraped. The files used are quickly explained below:
- `mb-id_2_name_and_am-id.py`: based on the musicbrainz_id get the name and the allmusic_id from the musicbrainz API whenever possible
- `name_2_am-id.py`: where the allmusic_id was not available in the muscbrainz API, take the allmusic_id of the artist that appears first when searching for the artist's name on allmusic.com
- `am-id_2_relatedArtist-html.py`: get HTML of #relatedArtists sub-webpage of all artists
- `am-id_2_songs-html.py`: get HTML of #songs sub-webpage of all artists
- `html_processing.py`: process HTML files to represent the most important information in a dataset
- `create_edges.py`: further process this dataset and create a list of edges betweeen artists