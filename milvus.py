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

def insert(collection_name, data):
  res = client.insert(
    collection_name=collection_name,
    data=data
  )
  return res

  # data={
  #   "hn_id": 39304736,
  #   "comment_count": 672,
  #   "title": "FCC rules AI-generated voices in robocalls illegal",
  #   "url": "https://www.fcc.gov/document/fcc-makes-ai-generated-voices-robocalls-illegal",
  #   "content": "The Federal Communications Commission (FCC) has adopted a ruling that defines calls made with AI-generated voices as 'artificial' under the Telephone Consumer Protection Act (TCPA). This means that such calls are subject to the act's restrictions on telemarketing and automated calls.",
  #   "vector_hn": result.embeddings[0]
  # }

def batch_insert(collection_name, data):
  res = client.insert(
    collection_name=collection_name,
    data=data
  )
  return res

# data = [
#   { ... },
#   { ... }
# ]
