import pandas as pd
import os
from datetime import datetime
from pprint import pprint
import ast

def convert_to_datetime(df):
  df['Date'] = pd.to_datetime(df['time'], unit='s')
  df['Processing Date'] = pd.to_datetime(df['processing_date'], unit='s')
  df.drop(columns=['time', 'processing_date'], inplace=True)
  return df

def get_list(x):
  return ast.literal_eval(x)

def get_dataframes_by_week():

  df = pd.read_csv(f'exports/export_{datetime.now().strftime("%Y-%m-%d")}.csv')
  df.drop(df.index[0], inplace=True) # csv header row

  df = convert_to_datetime(df)
  all_dates_by_week = pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='W-MON')

  for i in range(len(all_dates_by_week)-1):
    start_date = all_dates_by_week[i]
    end_date = all_dates_by_week[i+1]

    week_df = df[(df['Date'] >= start_date) & (df['Date'] < end_date)]
    
    week_df.to_csv(f'exports/weekly/weekly_{start_date.strftime("%Y-%m-%d")}.csv', index=False)

def get_articles_per_week():
  data = []
  for file in os.listdir('exports/weekly'):
    df = pd.read_csv(f'exports/weekly/{file}')

    # create a new dataframe with the count of articles per week
    count = df['id'].count()
    date = file.split('_')[1].split('.')[0]
    data.append({'Date': date, 'Count': count})

  return pd.DataFrame(data, columns=['Date', 'Count'])

def get_keywords_per_day():
  data = []
  df = pd.read_csv(f'exports/export_{datetime.now().strftime("%Y-%m-%d")}.csv')
  df.drop(df.index[0], inplace=True) # csv header row

  df = convert_to_datetime(df)
  all_dates_by_day = pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='D', unit='s')

  for date in all_dates_by_day:
    keywords = {}
    # get all articles published on that day
    day_df = df[df['Date'].dt.date == date.date()]
    for index, row in day_df.iterrows():
      for keyword in get_list(row['keywords']):
        if keyword in keywords:
          keywords[keyword] += 1
        else:
          keywords[keyword] = 1


    data.append({'Date': date, 'Keywords': keywords})
    
  return pd.DataFrame(data, columns=['Date', 'Keywords'])

def get_mentions_per_day(keyword):
  df = get_keywords_per_day()
  keyword_mentions = []
  for index, row in df.iterrows():
    if keyword in row['Keywords']:
      keyword_mentions.append({'Date': row['Date'], f'{keyword} mentions': int(row['Keywords'][keyword])})

  return pd.DataFrame(keyword_mentions, columns=['Date', f'{keyword} mentions'])