for name in mb-song-id_search_*
do
  newname=song_"$(echo "$name" | cut -c19-)"
  mv "$name" "$newname"
done
