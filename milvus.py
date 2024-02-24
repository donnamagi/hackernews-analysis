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
    collection_name= 'Newsletter',
    data=data
  )
  return res

def delete(ids):
  res = client.delete(
    collection_name= 'Newsletter',
    pks=ids 
  )
  return res

def search_vector(vectors, fields = OUTPUT_FIELDS, limit=RES_LIMIT):
  res = client.search(
    collection_name= 'Newsletter',
    data=vectors, # [0.1, 0.2, ...], [0.3, 0.4, ...] etc for bulk search
    filter="content != ''",
    output_fields= fields,
    limit=limit
  )
  return res[0]

def search_query(query, fields = OUTPUT_FIELDS, limit=RES_LIMIT):
  res = client.query(
    collection_name= 'Newsletter',
    filter=query, # ''
    output_fields= fields,
    limit=limit
  )
  return res

def search_get(ids):
  res = client.get(
    collection_name= 'Newsletter',
    ids=ids #[1, 2, 3, ...]
  )
  return res
