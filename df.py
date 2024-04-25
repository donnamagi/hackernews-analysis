import pandas as pd
from milvus import get_all_db_data
from collections import Counter
import ast
from datetime import datetime
from utils import convert_to_datetime

def get_all_keywords(df: pd.DataFrame):
  all_keywords = []
  for keywords_str in df['keywords']:
    if type(keywords_str) == float: # NaN
      continue
    try:
      keywords = ast.literal_eval(keywords_str)
      all_keywords.extend(keywords)
    except:
      print(f"Error parsing: {keywords_str}")
  return all_keywords

def count_keywords(keywords: list):
  return Counter(keywords).most_common()

def new_csv():
  results = get_all_db_data()
  df = pd.DataFrame(results)

  # for the dataset demo readability
  # turn unix timestamps into datetime objects 
  # df = convert_to_datetime(df)

  csv_file_path = f'exports/export_{datetime.now().strftime("%Y-%m-%d")}.csv'
  df.to_csv(csv_file_path, index=False)

def new_keywords_csv(keywords):
  df = pd.DataFrame(keywords, columns=['keyword', 'frequency'])
  csv_file_path = f'exports/keywords_{datetime.now().strftime("%Y-%m-%d")}.csv'
  df.to_csv(csv_file_path, index=False)

def main():
  try:
    df = pd.read_csv(f'exports/export_{datetime.now().strftime("%Y-%m-%d")}.csv')
  except FileNotFoundError:
    new_csv()
    df = pd.read_csv(f'exports/export_{datetime.now().strftime("%Y-%m-%d")}.csv')

  kw = count_keywords(get_all_keywords(df))
  if input("Do you want to save the keywords in a csv file? (y/n): ") == 'y':
    new_keywords_csv(kw) 
  else:
    print("Exiting.")

main()
