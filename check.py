from milvus import search_vector
from embeddings import get_embedding
import pprint

def search(input):
  vector = get_embedding(input)
  return search_vector(vectors=[vector])

def main():
  user_input = input("Enter a search query: ")
  results = search(user_input)
  pprint.pprint(results)

main()
