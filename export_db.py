from milvus import search_query
import json
from datetime import datetime
import numpy as np
from pprint import pprint

# This script exports the data from the Milvus collection to a JSON file.
# Basically a backup of the DB before trying something new.

if __name__ == '__main__':
  try:
    res = search_query(
      query="id > 0",
      fields=["id", "title", "keywords", "vector", "url", "content", "comment_ids", "date"],
      limit=1000
    )
    print(f"Exported {len(res)} items.")

    # convert float32 to float64 for JSON serialization
    for item in res:
      if isinstance(item['vector'][0], np.float32):
        item['vector'] = [float(float32) for float32 in item['vector']]

    # create a timestamped file for the backup
    with open(f'backups/{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
      f.write(json.dumps(res, indent=2))
  except TypeError as e:
    print(f"Error: {e}")
