from pymilvus import MilvusClient
from dotenv import load_dotenv
import os

load_dotenv()
CLUSTER_ENDPOINT = os.getenv("MILVUS_CLUSTER_ENDPOINT")
TOKEN = os.getenv("MILVUS_API_KEY")

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
