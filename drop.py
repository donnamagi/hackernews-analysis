from milvus import delete, get_all_db_records

def main():
  results = get_all_db_records()
  
  ids = [item['id'] for item in results]
  print(f"Deleting {len(ids)} items.")
  delete(ids)

main()
