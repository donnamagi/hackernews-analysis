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
