
import pandas as pd
from milvus import search_query
from collections import Counter
import ast

def get_all_keywords(df: pd.DataFrame):
  all_keywords = []
  for keywords_str in df['keywords_normalized']:
    keywords = ast.literal_eval(keywords_str)
    all_keywords.extend(keywords)
  return all_keywords

def count_keywords(keywords: list):
  keywords_freq = Counter(keywords)
  for keyword, freq in keywords_freq.most_common():
      print(f'{keyword}: {freq}')

# results = search_query(query= "id > 0", fields = ['id', 'keywords', 'date'], limit=1000)

# df = pd.dfFrame(results)

# # Export to CSV
# csv_file_path = 'export.csv'
# df.to_csv(csv_file_path, index=False)

# print('data exported')

# Function to rename similar keywords for consistency
def rename_keywords(keywords: list):
    renamed_list = []
    for keyword in keywords:
        if keyword == "Microframework":
            renamed_list.append("Microframeworks")
        elif keyword == "Modularity":
            renamed_list.append("Modularity")
        elif keyword == "Code minimalism":
            renamed_list.append("Minimalism")
        else:
            renamed_list.append(keyword)
    return renamed_list


def set_new_keywords(df: pd.DataFrame):
  # Assuming 'keywords' column is already a list. If not, ensure conversion from string to list where needed.
  df['keywords_normalized'] = df['keywords'].apply(rename_keywords)
  return df

def main():
  df = pd.read_csv('export_normalized.csv')
  # count_keywords(get_all_keywords(df))
  # df['keywords'] = df['keywords'].apply(lambda x: eval(x) if pd.notnull(x) else [])
  
  # # Apply the keyword normalization
  # df = set_new_keywords(df)
  
  # # Demonstrate the outcome
  # print(df[['keywords', 'keywords_normalized']].head())
  # df.to_csv('export_normalized.csv', index=False)
  count_keywords(get_all_keywords(df))
   

main()
