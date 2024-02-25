import requests

# Hacker News API 
  
def get_best_stories():
  url = 'https://hacker-news.firebaseio.com/v0/beststories.json?print=pretty'

  response = requests.get(url)
  if response.status_code == 200:
    return response.json()
  else:
    print(f"Error fetching data: {response.status_code}")

def get_top_stories():
  url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'

  response = requests.get(url)
  if response.status_code == 200:
    return response.json()
  else:
    print(f"Error fetching data: {response.status_code}")

def get_hn_story(story_id):
  url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty'

  response = requests.get(url)
  if response.status_code == 200:
    return response.json()
  else:
    print(f"Error fetching data: {response.status_code}")
