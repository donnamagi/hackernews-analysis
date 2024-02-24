
import pandas as pd
from milvus import search_query
from collections import Counter
import ast

df = pd.read_csv('export.csv')

all_keywords = []
for keywords_str in df['keywords']:
  keywords = ast.literal_eval(keywords_str)
  all_keywords.extend(keywords)
print(all_keywords)

keywords_freq = Counter(all_keywords)
for keyword, freq in keywords_freq.most_common():
    print(f'{keyword}: {freq}')

# results = search_query(query= "id > 0", fields = ['id', 'keywords', 'date'], limit=1000)

# df = pd.dfFrame(results)

# # Export to CSV
# csv_file_path = 'export.csv'
# df.to_csv(csv_file_path, index=False)

# print('data exported')
