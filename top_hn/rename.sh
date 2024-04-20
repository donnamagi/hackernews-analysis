#!/bin/bash

directory="$HOME/documents/projects/semantic/top_hn"
cd "$directory"

# looking for pattern "dd-mm-yyyy.json"
for file in ??-??-????.json; do
  day="${file:0:2}"
  month="${file:3:2}"
  year="${file:6:4}"

  new_filename="${year}-${month}-${day}.json"
  cp "$file" "$new_filename"
  echo "Renamed $file to $new_filename"

  # remove old file
  rm "$file"
  echo "Removed $file"
done
