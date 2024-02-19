from pymilvus import MilvusClient
from dotenv import load_dotenv
import os
import pprint

load_dotenv()
CLUSTER_ENDPOINT = os.getenv("MILVUS_CLUSTER_ENDPOINT")
TOKEN = os.getenv("MILVUS_API_KEY")

client = MilvusClient(
    uri=CLUSTER_ENDPOINT,
    token=TOKEN 
)

res = client.describe_collection(
    collection_name='Newsletter'
)

pprint.pprint(res)
