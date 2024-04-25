import pandas as pd
from collections import Counter
from utils import get_week_start_end_dates
from datetime import datetime
import spacy
import ast

nlp = spacy.load('en_core_web_sm')
TOP_KEYWORDS_AMOUNT = 30
EVAL_COUNT = 15

def get_all_companies_per_week():
  all_dates_by_week = get_week_start_end_dates()

  date_ranges = list(zip(all_dates_by_week[:-1], all_dates_by_week[1:])) 
  date_ranges_named = [f"{start.date().strftime('%m.%d')} - {end.date().strftime('%m.%d')}" for start, end in date_ranges]  

  df = pd.read_csv(f'exports/export_2024-04-25.csv')
  weekly_keywords = []
  df['time'] = pd.to_datetime(df['time'], unit='s')

  for start, end in date_ranges:
      mask = (df['time'].dt.date >= start.date()) & (df['time'].dt.date < end.date())
      filtered_df = df[mask]

      if not filtered_df.empty:
          filtered_keywords = []
          for keywords in filtered_df['keywords']:
              keywords = ast.literal_eval(keywords)
              filtered_keywords.extend(keywords)
          weekly_keywords.append(filtered_keywords)
      else:
          weekly_keywords.append([])

  weekly_keyword_counts = [Counter(keywords) for keywords in weekly_keywords]

  top_weekly = {}
  # sort them by count
  for i, keyword_count in enumerate(weekly_keyword_counts):
    top_weekly[i] = keyword_count.most_common(EVAL_COUNT)

  # name the weeks
  top_weekly = {date_ranges_named[i]: top_weekly[i] for i in range(len(date_ranges_named))}

  # filter out abbreviations and non-organizations
  COMMON_ABBREVIATIONS = ['AI', 'ML', 'CSS', 'API', 'GPU', 'CPU', 'CUDA', 'IP', 'SQL', 
                          'SSH', 'JIT', 'EU', 'Xz', 'AMD', 'Interpretable ML']
  def is_organization(keyword):
    if keyword in COMMON_ABBREVIATIONS:
      return False
    doc = nlp(keyword)
    for ent in doc.ents:
      if ent.label_ == 'ORG':
        return True
    return False

  top_weekly_orgs = {}
  for week, keywords in top_weekly.items():
    for keyword, count in keywords:
      if is_organization(keyword):
        if week not in top_weekly_orgs:
          top_weekly_orgs[week] = [(keyword, count)]
        else:
          top_weekly_orgs[week].append((keyword, count))

  # lists need to be the same length for the df. adding empty tuples where needed
  max_len = max(len(keywords) for keywords in top_weekly_orgs.values())
  for week, keywords in top_weekly_orgs.items():
    if len(keywords) < max_len:
      top_weekly_orgs[week].extend([('', '')] * (max_len - len(keywords)))

  # finding all unique organizations in the dict
  all_orgs = set()
  for week, keywords in top_weekly_orgs.items():
    for keyword, count in keywords:
      if keyword != '':
        all_orgs.add(keyword)

  rows = list(all_orgs)
  columns = ['Week'] + rows

  # making rows weeks and columns the mentions of specific orgs
  data = []
  for week, keywords in top_weekly_orgs.items():
    row = [week]
    for org in all_orgs:
      for keyword, count in keywords:
        if keyword == org:
          row.append(count)
          break
      else:
        row.append(0)
    data.append(row)

  df = pd.DataFrame(data, columns=columns)
  long_format_df = pd.melt(df, id_vars=['Week'], var_name='Company', value_name='Mentions')

  csv_file_path = f'exports/weekly_companies_{datetime.now().strftime("%Y-%m-%d")}.csv'
  df.to_csv(csv_file_path, index=False)

  long_csv_file_path = f'exports/weekly_companies_long_{datetime.now().strftime("%Y-%m-%d")}.csv'
  long_format_df.to_csv(long_csv_file_path, index=False)

  return df, long_format_df

def get_companies_per_week(companies : list, df : pd.DataFrame):
  # only keep the columns that are in the list
  df = df[['Week'] + companies]
  return df
