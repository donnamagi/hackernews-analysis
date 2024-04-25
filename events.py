import pandas as pd
from utils import get_mentions_per_day

def get_events():
  events = [
    {
      'title': 'XZ Backdoor attack discovered',
      'annotations': [('Mar 29, 2024', 'XZ Backdoor attack discovered on March 29th')],
      'keywords': ['Security', 'Backdoor', 'Open source', 'XZ', 'Xz']
    },
    {
      'title': "Apple's conflict with Spotify and Epic Games",
      'annotations': [
        ('Mar 04, 2024', 'EU announces 1.8 billion fine for Apple on March 4th'),
        ('Mar 06, 2024', 'Apple terminates developer account of Epic Games on March 6th'),
        ],
      'keywords': ['Apple', 'Epic Games', 'Fortnite', 'The Digital Markets Act', 'App Store', 'Spotify', 'Lawsuit']
    },
    {
      'title': "Google's LLM release",
      'annotations': [('Feb 15, 2024', 'Gemini AI announces the release of LLM on February 15th')],
      'keywords': ['Gemini', 'Google', 'Racial representation', 'Historical accuracy', 'Misinformation', 'Safety']
    }
  ]

  for event in events:
    # total sum of keyword mentions
    mentions_df = get_mentions_per_day(event['keywords'])
    mentions_df['Total mentions'] = mentions_df[event['keywords']].sum(axis=1)
    event['df'] = mentions_df

    # annotations to df
    annotations_df = pd.DataFrame(event['annotations'], columns=["date", "event"])
    annotations_df.date = pd.to_datetime(annotations_df.date)
    annotations_df["Total mentions"] = mentions_df['Total mentions'].max()
    event['annotations'] = annotations_df

  return events
