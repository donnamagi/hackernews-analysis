from milvus import insert, get_all_db_ids
from hackernews import get_hn_story
from scrape import scrape_content, call_ollama, clean_text
from keywords import get_keywords
from embeddings import get_embedding
from datetime import datetime
import os
import json

def main():
  collection = get_collection_ids() # get ids from db
  new_articles = get_json_ids() # ids to be processed

  for date, ids in new_articles.items():
    process_collection(collection, ids, date)

def process_collection(collection, ids, date):
  for id in ids:
    if id not in collection:
      process_entry(id, date)
      collection.add(id)
    else:
      print(f"{id} already in collection.")

def process_entry(id, date):
  story = get_hn_story(id)
  print(f"\n\n Processing {story['id']} - {story['title']}")

  content = story.get('text')
  if content is None:
    # no HN comment, so I scrape the url
    content = scrape_content(story['url'])
  if content:
    content = summarize_content(content)
    vector = get_embedding(content)
    keywords = get_keywords(content) 

    print(f"Keywords: {keywords}")
  else:
    # fallback to title as the embedding
    vector = get_embedding(story['title'])
    keywords = get_keywords(story['title'])

  # add data to the entry
  story['vector'] = vector
  story['keywords'] = keywords
  story['content_summary'] = content
  story['processing_date'] = unix(date)

  try:
    return add_to_collection(story)
  except Exception as e:
    print(f"Error: {e}")


def summarize_content(content):
  if content:
    content = clean_text(content[:2000]) 
    content = clean_text(call_ollama(content)) # since ollama likes to yap
    print(f"\n\n Summary: {content} \n\n")
    return content
  return None # can't scrape, no HN comment

def add_to_collection(story):
  if insert(story):
    print(f"Added {story['id']} to collection.")
    return True
  return False

def get_collection_ids():
  ids = set()

  res = get_all_db_ids()

  for item in res:
    ids.add(item['id'])
  return ids

def get_json_ids():
  ids_per_date = dict()
  json_files = [file for file in os.listdir('top_hn') if file.endswith('.json')]

  for file in json_files:
    file_path = os.path.join('top_hn', file)
    with open(file_path, 'r') as f:
      data = json.load(f)
      date = file.split('.')[0]
      json_ids = data[:30]
      ids_per_date[date] = json_ids

  return ids_per_date

def unix(date_string):
  date_obj = datetime.strptime(date_string, '%Y-%m-%d')
  unix_timestamp = int(datetime.timestamp(date_obj))
  return unix_timestamp

if __name__ == "__main__":
  main()
