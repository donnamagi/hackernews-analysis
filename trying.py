import pandas as pd
from collections import Counter
from utils import get_week_start_end_dates
from datetime import datetime
import spacy
import ast

nlp = spacy.load('en_core_web_sm')
TOP_KEYWORDS_AMOUNT = 20
EVAL_COUNT = 10

def main():
  all_dates_by_week = get_week_start_end_dates()

  date_ranges = list(zip(all_dates_by_week[:-1], all_dates_by_week[1:])) 
  date_ranges_named = [f"{start.date()} - {end.date()}" for start, end in date_ranges]  



  df = pd.read_csv(f'exports/export_{datetime.now().strftime("%Y-%m-%d")}.csv')
  weekly_keywords = []
  df['time'] = pd.to_datetime(df['time'], unit='s')

  for start, end in date_ranges:
      mask = (df['time'].dt.date >= start.date()) & (df['time'].dt.date < end.date())
      filtered_df = df[mask]

      if not filtered_df.empty:
          filtered_keywords = []
          for keywords in filtered_df['keywords']:
              if isinstance(keywords, str):
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

  # get descriptive keywords
  COMMON_ABBREVIATIONS = ['AI', 'ML', 'CSS', 'API', 'GPU', 'SQL']
  def is_organization(keyword):
    if keyword in COMMON_ABBREVIATIONS:
      return False
    doc = nlp(keyword)
    for ent in doc.ents:
      if ent.label_ == 'ORG':
        return True
    return False

  top_5_weekly_orgs = {}
  for week, keywords in top_weekly.items():
    for keyword, count in keywords:
      if is_organization(keyword):
        if week not in top_5_weekly_orgs:
          top_5_weekly_orgs[week] = [(keyword, count)]
        else:
          top_5_weekly_orgs[week].append((keyword, count))

  # lists need to be the same length for the df. adding empty tuples where needed
  max_len = max(len(keywords) for keywords in top_5_weekly_orgs.values())
  for week, keywords in top_5_weekly_orgs.items():
    if len(keywords) < max_len:
      top_5_weekly_orgs[week].extend([('', '')] * (max_len - len(keywords)))

  # finding all unique organizations in the dict
  all_orgs = set()
  for week, keywords in top_5_weekly_orgs.items():
    for keyword, count in keywords:
      if keyword != '':
        all_orgs.add(keyword)

  rows = list(all_orgs)
  columns = ['Week'] + rows

  # making rows weeks and columns the mentions of specific orgs
  data = []
  for week, keywords in top_5_weekly_orgs.items():
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

  return df

