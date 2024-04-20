#!/bin/bash

url="https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty"

directory="$HOME/documents/projects/semantic/top_hn"
file_name="$(date "+%Y-%m-%d").json"

if [ ! -f "${directory}/${file_name}" ]; then
  # body + status code
  http_status=$(curl -s -o "${directory}/${file_name}" -w "%{http_code}" "$url")

  if [ "$http_status" -eq 200 ]; then
    echo "success"
  else
    # removing empty file
    rm -f "${directory}/${file_name}"
    echo "error"
  fi
else
  echo "File for today already exists."
fi

# cron job
# 0 8 * * * $HOME/documents/projects/semantic/top_hn/fetch_best.sh
