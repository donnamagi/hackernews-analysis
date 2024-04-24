import pandas as pd
from utils import get_list, convert_to_datetime
from hackernews import get_hn_story

df = pd.read_csv(f'exports/export_2024-04-24.csv')

apple_df = df[df['keywords'].str.contains('Apple', case=False, na=False)]
nvidia_df = df[df['keywords'].str.contains('Nvidia', case=False, na=False)]


def google_df():
  google_df = df[df['keywords'].str.contains('Google', case=False, na=False)]
  google_df = convert_to_datetime(google_df)

  google_comments = {}
  for index, row in google_df.iterrows():
    commentslist = get_list(row['kids'])
    for id in commentslist:
      google_comments['Date'] = row['date']
      google_comments['ID'] = id
      google_comments['Comment'] = get_hn_story(id)

  google_df = pd.DataFrame(google_comments, columns=['Date', 'ID', 'Comment'])


google_df()