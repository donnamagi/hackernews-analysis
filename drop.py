from milvus import search_query, delete
from datetime import datetime
import pandas as pd

def main():
  results = search_query(query= "date == '15-03-2024'", fields = ['id', 'vector'], limit=1000)
  # keep_vectors(results)

  if len(results) == 0:
    return print("No items found.")
  
  ids = [item['id'] for item in results]
  print(f"Deleting {len(ids)} items.")
  delete(ids)

def keep_vectors(results):
  # store the vectors in a dict with the ID to not waste API tokens
  vectors = dict()
  for item in results:
    vectors[item['id']] = item['vector']

  print(f"Storing {len(vectors)} vectors.")
  df = pd.DataFrame(vectors.items(), columns=['id', 'vector'])

  csv_file_path = f'vectors_{datetime.now().strftime("%d-%m-%Y")}.csv'
  df.to_csv(csv_file_path, index=False)

main()
