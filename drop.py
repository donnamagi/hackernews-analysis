from milvus import search_query, delete

def main():
  results = search_query(query= "date == '15-03-2024'", fields = ['id', 'vector'], limit=1000)


  if len(results) == 0:
    return print("No items found.")
  
  ids = [item['id'] for item in results]
  print(f"Deleting {len(ids)} items.")
  delete(ids)

main()
