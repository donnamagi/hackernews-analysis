import voyageai
from dotenv import load_dotenv
import os

load_dotenv()
VOYAGE_KEY = os.getenv("VOYAGE_API_KEY")

def get_embedding(text):
  vo = voyageai.Client(api_key = VOYAGE_KEY)
  result = vo.embed(text, model="voyage-2")
  return result.embeddings[0]
