from milvus import search_query, delete

def main():
  results = search_query(query= "id > 0", fields = ['id', 'keywords', 'date'], limit=1000)
  ids = [item['id'] for item in results]
  print(f"Deleting {len(ids)} items.")
  delete(ids)

main()
