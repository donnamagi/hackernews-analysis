from fastapi import APIRouter
from pymilvus import MilvusClient
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel
import os

load_dotenv()

CLUSTER_ENDPOINT = os.getenv("MILVUS_CLUSTER_ENDPOINT")
TOKEN = os.getenv("MILVUS_API_KEY")
OUTPUT_FIELDS = ['hn_id', 'title', 'content', 'date', 'url']

client = MilvusClient(CLUSTER_ENDPOINT, TOKEN)


router = APIRouter(prefix="/milvus", tags=["Milvus"])

class IdsRequest(BaseModel):
  ids: List[int]

class VectorSearchRequest(BaseModel):
  vectors: List[List[float]]
  query: str = "content != ''"
  fields: List[str] = OUTPUT_FIELDS
  limit: int = 5

class SearchRequest(BaseModel):
  query: str
  fields: List[str] = OUTPUT_FIELDS
  limit: int = 5

@router.post("/insert")
def insert(data):
  res = client.insert(
    collection_name='HackerNews',
    data=data
  )
  return res

@router.delete("/delete")
def delete(request: IdsRequest):
  res = client.delete(
    collection_name='HackerNews',
    pks=request.ids
  )
  return res

@router.get("/search/{id}")
def get_one(id: int):
  res = client.get(
    collection_name='HackerNews',
    ids=[id]
  )
  return res

@router.post("/search")
def get_many(request: IdsRequest):
  res = client.get(
    collection_name='HackerNews',
    ids=request.ids
  )
  return res

@router.post("/search_vector")
def search_vector(request: VectorSearchRequest):
  res = client.search(
    collection_name='HackerNews',
    data=request.vectors,
    filter=request.query,
    output_fields=request.fields,
    limit=request.limit
  )
  return res[0]

@router.post("/search_query")
def search_query(request: SearchRequest):
  res = client.query(
    collection_name='HackerNews',
    filter=request.query,
    output_fields=request.fields,
    limit=request.limit
  )
  return res

@router.get("/all")
def get_all_db_ids():
  res = client.query(
    collection_name='HackerNews',
    filter="id > 0",
    output_fields=["id"],
    limit=1000
  )
  if len(res) == 1000:
    return "Limit reached. Only first 1000 items returned."
  return res
