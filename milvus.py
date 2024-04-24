from pymilvus import MilvusClient
from dotenv import load_dotenv
import os

load_dotenv()
CLUSTER_ENDPOINT = os.getenv("MILVUS_CLUSTER_ENDPOINT")
TOKEN = os.getenv("MILVUS_API_KEY")

RES_LIMIT = 5
OUTPUT_FIELDS = ['hn_id', 'title', 'content', 'date', 'url']

client = MilvusClient(
    uri=CLUSTER_ENDPOINT,
    token=TOKEN 
)

def insert(data):
  res = client.insert(
    collection_name= 'HackerNews',
    data=data
  )
  return res

def delete(ids):
  res = client.delete(
    collection_name= 'HackerNews',
    pks=ids 
  )
  return res

def search_vector(vectors, fields = OUTPUT_FIELDS, limit=RES_LIMIT):
  res = client.search(
    collection_name= 'HackerNews',
    data=vectors, # [0.1, 0.2, ...], [0.3, 0.4, ...] etc for bulk search
    filter="content != ''",
    output_fields= fields,
    limit=limit
  )
  return res[0]

def search_query(query, fields = OUTPUT_FIELDS, limit=RES_LIMIT):
  res = client.query(
    collection_name= 'HackerNews',
    filter=query, # ''
    output_fields= fields,
    limit=limit
  )
  return res

def search_get(ids):
  res = client.get(
    collection_name= 'HackerNews',
    ids=ids #[1, 2, 3, ...]
  )
  return res

def get_all_db_ids():
  res = client.query(
    collection_name= 'HackerNews',
    filter="id > 0",
    output_fields= ["id"],
    limit=1000
  )
  if len(res) == 1000:
    return print("Limit reached. Only first 1000 items returned.")
  return res

def get_all_db_data():
  res = client.query(
    collection_name= 'HackerNews',
    filter="id > 0",
    output_fields= ["id", "title", "keywords", "url", "content_summary", "time", "processing_date", "score", "type"],
    limit=1000
  )
  if len(res) == 1000:
    return print("Limit reached. Only first 1000 items returned.")
  return res

#maybe do smth like compare what got most attention during the period?

def get_all_with_comments():
  res = client.query(
    collection_name= 'HackerNews',
    filter="id > 0",
    output_fields= ["id", "title", "keywords", "time", "score", "kids"],
    limit=1000
  )
  if len(res) == 1000:
    return print("Limit reached. Only first 1000 items returned.")
  return res
