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

  # data={
  #   "hn_id": 39304736,
  #   "comment_ids": [],
  #   "title": "FCC rules AI-generated voices in robocalls illegal",
  #   "url": "https://www.fcc.gov/document/fcc-makes-ai-generated-voices-robocalls-illegal",
  #   "content": "The Federal Communications Commission (FCC) has adopted a ruling that defines calls made with AI-generated voices as 'artificial' under the Telephone Consumer Protection Act (TCPA). This means that such calls are subject to the act's restrictions on telemarketing and automated calls.",
  #   "vector": result.embeddings[0]
  #   "hn_comment": "",
  #   "date": "11-10-2021",
  # }

def batch_insert(data):
  res = client.insert(
    collection_name= 'Newsletter',
    data=data
  )
  return res

# data = [
#   { ... },
#   { ... }
# ]

def search_vector(vectors):
  res = client.search(
    collection_name= 'Newsletter',
    data=vectors, # [0.1, 0.2, ...], [0.3, 0.4, ...] etc for bulk search
    filter="content != ''",
    output_fields=OUTPUT_FIELDS,
    limit=RES_LIMIT
  )
  return res[0]

def search_query(query):
  res = client.query(
    collection_name= 'Newsletter',
    filter=query, # ''
    output_fields=OUTPUT_FIELDS,
    limit=RES_LIMIT
  )
  return res

def search_get(ids):
  res = client.get(
    collection_name= 'Newsletter',
    ids=ids #[1, 2, 3, ...]
  )
  return res
