from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import APIRouter
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = APIRouter(prefix="/hn", tags=["Hacker News"])

HN_BASE_URL = "https://hacker-news.firebaseio.com/v0"
MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db = client['hackernews']['source-data']

@app.get("/insert/all") 
async def insert_all_recents_to_db():
  top_stories = requests.get(f"{HN_BASE_URL}/topstories.json")
  new_stories = requests.get(f"{HN_BASE_URL}/newstories.json")
  ask_stories = requests.get(f"{HN_BASE_URL}/askstories.json")

  try:
    db.insert_one(
      {
        "top_stories": top_stories.json(), 
        "new_stories": new_stories.json(), 
        "ask_stories": ask_stories.json(),
        "timestamp": datetime.now().isoformat()
      }
    )

    return {
      "top_stories": bool(top_stories),
      "new_stories": bool(new_stories),
      "ask_stories": bool(ask_stories)
    }
  except Exception as e:
    print(e)


@app.get("/item/{item_id}")
async def insert_item(item_id: int):
  response = requests.get(f"{HN_BASE_URL}/item/{item_id}.json")
  try:
    db.insert_one(
      {
        response.json()
      }
    )
  except Exception as e:
    print(e)
  return response.json()
