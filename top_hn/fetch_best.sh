#!/bin/bash

url="https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty"

directory="$HOME/documents/projects/semantic/top_hn"
file_name="$(date "+%d-%m-%Y").json"

if [ ! -f "${directory}/${file_name}" ]; then
  # Use curl to send the GET request and save the response
  curl -s "$url" > "${directory}/${file_name}"
else
  echo "File for today already exists."
fi

# cron job
# 0 8 * * * $HOME/documents/projects/semantic/top_hn/fetch_best.sh
