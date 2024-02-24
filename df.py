import pandas as pd
from milvus import search_query
from collections import Counter
import ast
from datetime import datetime

def get_all_keywords(df: pd.DataFrame):
  all_keywords = []
  for keywords_str in df['keywords']:
    keywords = ast.literal_eval(keywords_str)
    all_keywords.extend(keywords)
  return all_keywords

def count_keywords(keywords: list):
  keywords_freq = Counter(keywords)
  for keyword, freq in keywords_freq.most_common():
      print(f'{keyword}: {freq}')

def new_csv():
  results = search_query(query= "id > 0", fields = ['id', 'keywords', 'date'], limit=1000)

  df = pd.DataFrame(results)

  csv_file_path = f'export_{datetime.now().strftime("%d-%m-%Y")}.csv'
  df.to_csv(csv_file_path, index=False)

def main():
  df = pd.read_csv('export.csv')
  count_keywords(get_all_keywords(df))

main()
