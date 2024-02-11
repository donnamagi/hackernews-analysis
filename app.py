import requests

url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'

response = requests.get(url)
if response.status_code == 200:
  top_stories = response.json()
else:
  print(f"Error fetching data: {response.status_code}")
  exit()

stories = dict()

for story_id in top_stories[:5]:
  story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty'
  story_response = requests.get(story_url)
  story_details = story_response.json()
  stories[story_id] = story_details

print(stories)
