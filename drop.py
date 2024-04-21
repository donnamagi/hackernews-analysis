from milvus import delete, get_all_db_ids

def main():
  results = get_all_db_ids()
  
  ids = [item['id'] for item in results]
  print(f"Deleting {len(ids)} items.")
  delete(ids)

main()
