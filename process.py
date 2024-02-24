import os
import json
from milvus import search_query, insert
from hackernews import get_hn_story
from scrape import scrape_content, call_ollama, clean_text
from keywords import get_keywords, get_orgs
from embeddings import get_embedding

def main():
  collection = get_collection_ids()
  data = get_json_ids()

  for date, ids in data.items():
    process_collection(collection, ids, date)

def process_collection(collection, ids, date):
  for id in ids:
    if id not in collection:
      process_entry(id, date)
    else:
      print(f"{id} already in collection.")

def process_entry(id, date):
  title, url, content, comments = get_data_from_hn(id)
  print(f"Processing {id} - {title}")
  
  if content is None:
    content = scrape_content(url)

  if content:
    content = summarize_content(content)
    vector = get_embedding(content)

    keywords = get_keywords(content) # ollama
    orgs = get_orgs(content) # spacy
    keywords = list(keywords.union(orgs)) # merge sets using union
    print(f"Keywords: {keywords}")
  else:
    vector = get_embedding(title)
    keywords = []

  return add_to_collection(
    id=id,
    title=title,
    keywords=keywords,
    vector=vector,
    url=url,
    content=content,
    comments=comments,
    date=date
  )

def get_data_from_hn(id):
  story = get_hn_story(id)
  title = story['title']
  url = story['url']
  content = story['text'] if 'text' in story else None
  comments = story['kids'] if 'kids' in story else []
  return title, url, content, comments

def summarize_content(content):
  if content:
    content = clean_text(content[:2000]) 
    content = clean_text(call_ollama(content)) # since ollama returns \n sometimes
    return content
  return None # can't scrape, no HN comment

def add_to_collection(id: int, vector: list, title: str, url: str, content: str, comments: list, date: str, keywords: list):
  data = {
    "id": id,
    "title": title,
    "keywords": keywords,
    "vector": vector,
    "url": url,
    "content": content,
    "comment_ids": comments,
    "date": date,
  }
  if insert(data):
    print(f"Added {id} to collection.")
    return True
  return False

def get_collection_ids():
  ids = set()

  res = search_query(
    query="id > 0", 
    fields=["id"], 
    limit=200
  )

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
      json_ids = data[:20]
      ids_per_date[date] = json_ids

  return ids_per_date

if __name__ == "__main__":
  main()
