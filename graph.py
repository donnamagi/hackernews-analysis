from milvus import search_vector, get_all_db_ids
import pandas as pd
from datetime import datetime
from pprint import pprint

def main():
  # get all vectors
  results = get_all_db_ids()

  # initialize an adjacency list
  adjacency_list = dict()
  for item in results:
    adjacency_list[item['id']] = []

  # compare all vectors
  for i in range(len(results)):
    similar = search_vector([results[i]['vector']])

    for item in similar: 
      if item['id'] != results[1]['id']:
        if item['distance'] > 0.85 and item['id'] not in adjacency_list[results[i]['id']]:
          adjacency_list[results[1]['id']].append(item['id'])
          adjacency_list[item['id']].append(results[i]['id'])

  pprint(adjacency_list)

  # save it in a csv file
  df = pd.DataFrame(adjacency_list.items(), columns=['id', 'vector'])
  csv_file_path = f'exports/adjacency_{datetime.now().strftime("%Y-%m-%d")}.csv'
  df.to_csv(csv_file_path, index=False)


main()
